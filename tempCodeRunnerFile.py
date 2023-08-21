modell=model.load_weights('./model2.h5')
results=modell.evaluate(test_images,verbose=0)
print("Loss: {:.4f}%".format(results[0]))
print("a: {:.4f}%".format(results[1]*100))