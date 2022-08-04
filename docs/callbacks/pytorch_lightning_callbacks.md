# Pytorch Lightning Callbacks

`pytorch_lightning` callbacks allows you to do energy tracking on model training,testing or prediction involving `pytorch_lightning` framework. 

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
from easyenergy.callbacks.pytorch_lightning import PerEpochCallback
cb = PerEpochCallback()
trainer = Trainer(
    epochs=epochs,
    callbacks=[cb])
trainer.fit(model, train_loader)
```

### 2) TrainCallback

Description: Callback to track energy usage from train begin to train end during model training. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.pytorch_lightning import TrainCallback
cb = TrainCallback()
trainer = Trainer(
    epochs=epochs,
    callbacks=[cb])
trainer.fit(model, train_loader)
```

### 3) TrainBatchCallback

Description: Callback to track energy usage from train begin to train end per batches during model training. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.pytorch_lightning import TrainBatchCallback
cb = TrainBatchCallback()
trainer = Trainer(
    epochs=epochs,
    callbacks=[cb])
trainer.fit(model, train_loader)
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
from easyenergy.callbacks.pytorch_lightning import TestCallback
cb = TestCallback()
trainer = Trainer(
    callbacks=[cb])
trainer.test(model, test_loader)
```
### 2) TestBatchCallback

Description: Callback to track energy usage from test begin to test end per batches during model evaluation. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.pytorch_lightning import TestBatchCallback
cb = TestBatchCallback()
trainer = Trainer(
    callbacks=[cb])
trainer.test(model, test_loader)
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
from easyenergy.callbacks.pytorch_lightning import PredictCallback
cb = PredictCallback()
trainer = Trainer(
    callbacks=[cb])
trainer.predict(model, test_loader)

```

### 2) PredictBatchCallback

Description: Callback to track energy usage from predict begin to predict end per batch during model inference. 

Arguments:   
Name | Input | Description 
 ----------- | ----------- |  -----------
output_dir | Optional, str | path to store output data in csv

Usage:   

```
from easyenergy.callbacks.pytorch_lightning import PredictBatchCallback
cb = PredictBatchCallback()
trainer = Trainer(
    callbacks=[cb])
trainer.predict(model, test_loader)

```



