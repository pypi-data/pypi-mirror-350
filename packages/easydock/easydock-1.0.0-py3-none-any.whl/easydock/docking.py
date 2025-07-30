from functools import partial
from multiprocessing import Pool

from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcNumRotatableBonds


def docking(mols, dock_func, dock_config, priority_func=CalcNumRotatableBonds, ncpu=1, dask_client=None, dask_report_fname=None):
    """

    :param mols: iterator of molecules, each molecule must have a title
    :param dock_func: docking function
    :param dock_config: yml-file with docking settings which will be passed to dock_func
    :param priority_func: function which return a numeric value, higher values - higher docking priority
    :param ncpu: number of cores to be used in a single server docking
    :param dask_client: reference to a dask client (if omitted single server docking will be performed)
    :param dask_report_fname: name of dask html-report file (optional)
    :return: iterator with molecule title and a dict of values returned by dock_func
    """
    Chem.SetDefaultPickleProperties(Chem.PropertyPickleOptions.AllProps)
    if dask_client is not None:
        from dask.distributed import as_completed, performance_report
        # https://stackoverflow.com/a/12168252/895544 - optional context manager
        from contextlib import contextmanager
        none_context = contextmanager(lambda: iter([None]))()
        with (performance_report(filename=dask_report_fname) if dask_report_fname is not None else none_context):
            nworkers = len(dask_client.scheduler_info()['workers'])
            futures = []
            for i, mol in enumerate(mols, 1):
                futures.append(dask_client.submit(dock_func, mol, priority=priority_func(mol), config=dock_config))
                if i == nworkers * 10:
                    break
            seq = as_completed(futures, with_results=True)
            for i, (future, (mol_id, res)) in enumerate(seq, 1):
                yield mol_id, res
                del future
                try:
                    mol = next(mols)
                    new_future = dask_client.submit(dock_func, mol, priority=priority_func(mol), config=dock_config)
                    seq.add(new_future)
                except StopIteration:
                    continue
    else:
        pool = Pool(ncpu)
        try:
            for mol_id, res in pool.imap_unordered(partial(dock_func, config=dock_config), tuple(mols), chunksize=1):
                yield mol_id, res
        finally:
            pool.close()
            pool.join()


def mol_dock(mol, config, program):
    """

    :param mol: RDKit Mol of a ligand with title
    :param config: yml-file with docking settings
    :return:
    """
    output = None


    mol_id = mol.GetProp('_Name')
    ligand_pdbqt_list = ligand_preparation(mol, boron_replacement=True)

    if ligand_pdbqt_list is None:
        return mol_id, None

    dock_output_conformer_list = []
    start_time = timeit.default_timer()
    for ligand_pdbqt in ligand_pdbqt_list:
        output_fd, output_fname = tempfile.mkstemp(suffix='_output.json', text=True)
        ligand_fd, ligand_fname = tempfile.mkstemp(suffix='_ligand.pdbqt', text=True)

        try:
            with open(ligand_fname, 'wt') as f:
                f.write(ligand_pdbqt)

            config = __parse_config(config)
            p = os.path.realpath(__file__)
            python_exec = sys.executable
            cmd = f'{python_exec} {os.path.dirname(p)}/vina_dock_cli.py -l {ligand_fname} -p {config["protein"]} ' \
                  f'-o {output_fname} --center {" ".join(map(str, config["center"]))} ' \
                  f'--box_size {" ".join(map(str, config["box_size"]))} ' \
                  f'-e {config["exhaustiveness"]} --seed {config["seed"]} --nposes {config["n_poses"]} -c {config["ncpu"]}'
            subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)  # this will trigger CalledProcessError and skip next lines)

            with open(output_fname) as f:
                res = f.read()
                if res:
                    res = json.loads(res)
                    mol_block = pdbqt2molblock(res['poses'].split('MODEL')[1], mol, mol_id)
                    output = {'docking_score': res['docking_score'],
                              'pdb_block': res['poses'],
                              'mol_block': mol_block}

                    dock_output_conformer_list.append(output)

        except subprocess.CalledProcessError as e:
            sys.stderr.write(f'Error caused by docking of {mol_id}\n')
            sys.stderr.write(str(e) + '\n')
            sys.stderr.write('STDERR output:\n')
            sys.stderr.write(e.stderr + '\n')
            sys.stderr.flush()

        finally:
            os.close(output_fd)
            os.close(ligand_fd)
            os.unlink(ligand_fname)
            os.unlink(output_fname)

    dock_time = round(timeit.default_timer() - start_time, 1)
    print \
        (f'[For Testing Only Sanity check]: There are {len(dock_output_conformer_list)} {mol_id} conformers that has been docked')
    print(f'\n')
    docking_score_list = [float(conformer_output['docking_score']) for conformer_output in dock_output_conformer_list]

    if not docking_score_list:
        return mol_id, None

    output = dock_output_conformer_list[docking_score_list.index(min(docking_score_list))]
    output['dock_time'] = dock_time

    return mol_id, output
