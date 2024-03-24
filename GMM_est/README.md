## Introduction

In this script, we generate fake data using different sets of parameters and save them as CSV files. We then discuss some notes and todos regarding the generated data.

## Data Generation

We generate fake data using the following parameters:

```
param_list = [[25,5,.5,.5,0,0],[20,5,.5,.5,0,0],[25,10,.5,.5,0,0],[25,5,.5,.1,0,0],[25,5,.1,.5,0,0],[25,5,.5,.5,3,3]]
```

For each set of parameters in the `param_list`, we generate three sets of data: `seq_result`, `active_result`, and `passive_result`. We generate a total of 10,000 observations for each set of data, with a variance of 5.

The generated data is then saved as CSV files:

```
seq_result.to_csv('fake_data/seq_data_%s.csv'%i)
active_result.to_csv('fake_data/active_data_%s.csv'%i)
passive_result.to_csv('fake_data/passive_data_%s.csv'%i)
```


## Logit demand

Note that for the logit results I use the following sets of files.

For wtp=25, lambda =5, beta1=beta2= .5 I use

```
fake_data_wtp_logit/seq_data_0.csv
fake_data_wtp_logit/active_data_0.csv
fake_data_wtp_logit/passive_data_0.csv
```

For wtp=30, lambda =5, beta1=.5 beta2= .3 I use

```
 fake_data_wtp_logit_fixed/seq_data_0.csv
fake_data_wtp_logit_fixed/seq_data_0.csv
fake_data_wtp_logit_fixed/seq_data_0.csv
```


For wtp=30, lambda =5, beta1=.45 beta2= .5 I use

```
 fake_data_wtp_logit_fixed/seq_data_1.csv
fake_data_wtp_logit_fixed/seq_data_1.csv
fake_data_wtp_logit_fixed/seq_data_.csv
```

### Logit parameter estimates

Parameter estimates for 


For
* wtp=30, lambda =5, beta1=.5 beta2= .3 
* wtp=30, lambda =5, beta1=.45 beta2= .5 I use

can be found in fake_params_logit_032224

## Notes

Here are some notes regarding the generated data:

- The test will likely reject the hypothesis when beta1=beta2, as there are not enough moment conditions to ensure a non-singular covariance matrix.
- The betas in the model do not appear to be identified.
- On average, p1 and p2 are the same according to the model, resulting in only 3 moment conditions.
- It may be worth considering only beta1 and beta2 and ignoring v, l, and mc.

## Todos

Here are some todos related to the generated data:

- There is an issue with the test when dealing with non-linearities, as they break the test.
- There is an issue with the test power in aggregating the dataframes incorrectly.