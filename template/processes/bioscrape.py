'''
Execute by running: ``python template/process/template_process.py``

TODO: Replace the template code to implement your own process.
'''

from __future__ import absolute_import, division, print_function

import os

from vivarium.core.process import Process
from vivarium.core.composition import (
    simulate_process_in_experiment,
    plot_simulation_output,
    PROCESS_OUT_DIR,
)

from bioscrape.types import Model
from bioscrape.simulator import DeterministicSimulator, ModelCSimInterface

# a global NAME is used for the output directory and for the process name
NAME = 'template'


# class ExpressionModel(Generator):
#     def __init__(self, config):
#         self.process1 = Bioscrape({'_parallel': True, 'sbml_file': 'model1.xml'})
#         self.process2 = Bioscrape({'_parallel': True, 'sbml_file': 'model2.xml'})
#         self.process3 = Bioscrape({'_parallel': True, 'sbml_file': 'model3.xml'})


class Bioscrape(Process):
    '''
    This mock process provides a basic template that can be used for a new process
    '''

    # give the process a name, so that it can register in the process_repository
    name = 'Bioscrape'

    # declare default parameters as class variables
    defaults = {
        'sbml_file': 'model.xml'}

    def __init__(self, initial_parameters=None):
        if initial_parameters is None:
            initial_parameters = {}

        super(Bioscrape, self).__init__(initial_parameters)

        # get the parameters out of initial_parameters if available, or use defaults
        self.sbml_file = self.parameters['sbml_file']
        self.model = Model(sbml_filename = self.sbml_file, sbml_warnings = False)

        # create the interface
        self.interface = ModelCSimInterface(self.model)

        # create a Simulator
        self.simulator = DeterministicSimulator()

    def ports_schema(self):
        '''
        ports_schema returns a dictionary that declares how each state will behave.
        Each key can be assigned settings for the schema_keys declared in Store:

        * `_default`
        * `_updater`
        * `_divider`
        * `_value`
        * `_properties`
        * `_emit`
        * `_serializer`
        '''

        return {
            'species': {
                species: {
                    '_default': 0.0,
                    '_updater': 'accumulate',
                    '_emit': True}
                for species in self.model.get_species()},

            'rates': {}}


    def next_update(self, timestep, states):
        self.interface.py_prep_deterministic_simulation()
        self.model.set_species(states['species'])

        import ipdb; ipdb.set_trace()



def run_bioscrape_process():
    '''Run a simulation of the process.

    Returns:
        The simulation output.
    '''
    # initialize the process by passing initial_parameters
    initial_parameters = {
        'sbml_file': 'Notebooks/model1.xml'}
    bioscrape_process = Bioscrape(initial_parameters)

    # run the simulation
    sim_settings = {'total_time': 10}
    output = simulate_process_in_experiment(bioscrape_process, sim_settings)

    # Return the data from the simulation.
    return output


def test_bioscrape_process():
    '''Test that the process runs correctly.

    This will be executed by pytest.
    '''
    output = run_bioscrape_process()
    # TODO: Add assert statements to ensure correct performance.


def main():
    '''Simulate the process and plot results.'''
    # make an output directory to save plots
    out_dir = os.path.join(PROCESS_OUT_DIR, NAME)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    output = run_bioscrape_process()

    # plot the simulation output
    plot_settings = {}
    plot_simulation_output(output, plot_settings, out_dir)


if __name__ == '__main__':
    main()
