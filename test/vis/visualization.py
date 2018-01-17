import model.forest_model as forest
import vis.visualization as vis

f = forest.ForestModel(10, 10, 0.8, 50, 0.6)
vis.show_virgin_type_map(f.current_state)

vis.run_model(50, 1000)
