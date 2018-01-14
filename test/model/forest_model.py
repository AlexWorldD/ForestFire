import model.forest_model as forest

f = forest.ForestModel(10, 10, 0.7)

assert f.current_state == f.init_state

