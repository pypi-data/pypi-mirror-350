#!/usr/bin/env python3

# Description
###############################################################################
""" Module to run the Extreme Gradient Boost algorithm. 

It is imported as:

import OCDocker.OCScore.XGBoost.OCxgboost as OCxgboost
"""

# Imports
###############################################################################

import numpy as np

from xgboost import XGBRegressor

# License
###############################################################################
'''
OCDocker
Authors: Rossi, A.D.; Torres, P.H.M.;
[The Federal University of Rio de Janeiro]
Contact info:
Carlos Chagas Filho Institute of Biophysics
Laboratory for Molecular Modeling and Dynamics
Av. Carlos Chagas Filho 373 - CCS - bloco G1-19,
Cidade Universitária - Rio de Janeiro, RJ, CEP: 21941-902
E-mail address: arturossi10@gmail.com
This project is licensed under Creative Commons license (CC-BY-4.0) (Ver qual)
'''

# Classes
###############################################################################


# Methods
###############################################################################

def run_xgboost(
        X_train : np.ndarray,
        y_train : np.ndarray,
        X_test : np.ndarray,
        y_test : np.ndarray,
        params : dict = {},
        verbose : bool = False
    ) -> tuple[XGBRegressor, float]:
    '''
    A function to train an XGBoost model and calculate the AUC score.

    Parameters
    ----------
    X_train : np.ndarray
        The training dataset.
    y_train : np.ndarray
        The training labels.
    X_test : np.ndarray
        The test dataset.
    y_test : np.ndarray
        The test labels.
    params : dict, optional
        The hyperparameters for the XGBoost model. Default is an empty dictionary.
    verbose : bool, optional
        Whether to print the training logs. Default is False.

    Returns
    -------
    model : XGBRegressor
        The trained XGBoost model.
    roc_auc : float
        The AUC score of the trained model.
    '''

    # Create the XGBoost model
    model = XGBRegressor(**params)

    # Train the model
    model.fit(
        X_train, 
        y_train, 
        eval_set = [(X_test, y_test)],
        verbose = verbose
    )

    # Get the AUC score
    evals_result = model.evals_result()
    metric = evals_result["validation_0"][params["eval_metric"].lower()][-1]

    # Return the trained model and the metric
    return model, metric
