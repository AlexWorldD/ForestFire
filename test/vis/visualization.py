import model.forest_model as forest
import vis.visualization as vis

f = forest.ForestModel(50, 50, 0.5, 50, 1.0)
vis.show_virgin_type_map(f.current_state)

vis.run_model(50, 500)
