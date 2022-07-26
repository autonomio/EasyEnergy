# Keras Callbacks

`kerascallbacks` allows you to do energy tracking on model training,testing or prediction involving `Keras` framework. 

## Training Callbacks.  
Callbacks to track energy usage while model is training.  

### 1) PerEpochCallback.  

Description: Callback to track energy usage per epoch during model training. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.keras import PerEpochCallback
cb = PerEpochCallback()
history = model.fit(x_train, y_train, epochs=epochs, callbacks=[cb])
```

### 2) TrainCallback

Description: Callback to track energy usage from train begin to train end during model training. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.keras import TrainCallback
cb = TrainCallback()
history = model.fit(x_train, y_train, epochs=epochs, callbacks=[cb])
```

### 3) TrainBatchCallback

Description: Callback to track energy usage from train begin to train end per batches during model training. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.keras import TrainBatchCallback
cb = TrainCallback()
history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, callbacks=[cb])
```

## Test Callbacks

Callbacks to track energy usage while doing model evaluation on the test set.

### 1) TestCallBack

Description: Callback to track energy usage from test begin to test end during model evaluation. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.keras import TestCallback
cb = TestCallback()
test = model.evaluate(x_test, y_test, callbacks=[cb])
```
### 2) TestBatchCallback

Description: Callback to track energy usage from test begin to test end per batches during model evaluation. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.keras import TestBatchCallback
cb = TestBatchCallback()
test = model.evaluate(x_test, y_test, batch_size=batch_size,
                      callbacks=[cb])
```

## Predict Callbacks

Callbacks to track energy usage while doing model inference.

### 1) PredictCallback

Description: Callback to track energy usage from predict begin to predict end during model inference. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.keras import PredictCallback
cb = PredictCallback()
pred = model.predict(x_test, callbacks=[cb])

```

### 2) PredictBatchCallback

Description: Callback to track energy usage from predict begin to predict end per batch during model inference. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.keras import PredictBatchCallback
cb = PredictBatchCallback()
pred = model.predict(x_test, batch_size=batch_size, callbacks=[cb])

```



