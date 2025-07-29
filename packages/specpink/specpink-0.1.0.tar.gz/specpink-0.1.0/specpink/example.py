from specpink.pipeline import Pipeline

# change according to needs
data_path = '../Data/prepared'
target_path_stacked = '../Data/stacked'
target_path_reduced = '../Data/reduced'
spectrum_path = '../Data/reduced/spectrum.txt'

# run pipeline
pipe = Pipeline(data_path, target_path_stacked, target_path_reduced, spectrum_path)
pipe.full()
