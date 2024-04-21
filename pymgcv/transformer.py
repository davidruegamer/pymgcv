import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import numpy as np
from rpy2.robjects import numpy2ri
numpy2ri.activate()

mgcv = importr('mgcv')

class SmoothConTransformer:
    def __init__(self, knots=None, absorb_cons=False, scale_penalty=True, 
                 null_space_penalty=False, sparse_cons=0, diagonal_penalty=False, 
                 apply_by=True, modCon=0):
        self.knots = knots
        self.absorb_cons = absorb_cons
        self.scale_penalty = scale_penalty
        self.null_space_penalty = null_space_penalty
        self.sparse_cons = sparse_cons
        self.diagonal_penalty = diagonal_penalty
        self.apply_by = apply_by
        self.modCon = modCon
        self.smooth_con_obj = None
          
    """
    Python class for R's mgcv::smoothCon objects
    
    Attributes:
    knots : Optional DataFrame supplying any knot locations for basis construction.
    absorb_cons : Boolean, set to True to have identifiability constraints absorbed into the basis.
    scale_penalty : Boolean, should the penalty coefficient matrix be scaled to have approximately
                    the same 'size' as the inner product of the terms model matrix with itself?
                    This can improve the performance of gamm fitting.
    null_space_penalty : Boolean, should an extra penalty be added to the smooth which will penalize
                         the components of the smooth in the penalty null space: provides a way of
                         penalizing terms out of the model altogether.
    apply_by : Boolean, set to False to have basis setup exactly as in default case, but to return
               an additional matrix X0 to the return object, containing the model matrix without
               the by variable, if a by variable is present. Useful for bam discrete method setup.
    sparse_cons : Integer, controls the type of sum to zero constraints used. If 0 then default sum
                  to zero constraints are used. If -1 then sweep and drop sum to zero constraints
                  are used (default with bam). If 1 then one coefficient is set to zero as
                  constraint for sparse smooths. If 2 then sparse coefficient sum to zero constraints
                  are used for sparse smooths. None of these options has an effect if the smooth
                  supplies its own constraint.
    diagonal_penalty : Boolean, if True then the smooth is reparameterized to turn the penalty into
                        an identity matrix, with the final diagonal elements zeroed (corresponding
                        to the penalty nullspace). May result in a matrix diagRP in the returned
                        object for use by PredictMat.
    modCon : Integer, force modification of any smooth supplied constraints. 0 - do nothing. 1 -
             delete supplied constraints, replacing with automatically generated ones. 2 - set fit
             and predict constraint to predict constraint. 3 - set fit and predict constraint to
             fit constraint.
    
    Returns:
    A modified smooth object or constructor from R's mgcv package.
    """
    
    def fit(self, obj, data, n=None):
        """
        Fit the SmoothCon model to the data.
        
        Parameters:
        obj : smooth specification object or a smooth object from R.
        data : data frame, model frame or list with the values of the covariates.
        n : number of values for each covariate (if data is a list).
        """
        
        if isinstance(data, pd.DataFrame):
            with localconverter(robjects.default_converter + pandas2ri.converter):
                r_data = robjects.conversion.py2rpy(data)
        else:
            raise TypeError("Data must be a pandas DataFrame")

        if n is None:
            n = data.shape[0]

# Prepare arguments with R-style naming (dots instead of underscores)
        r_args = {
            'absorb.cons': self.absorb_cons,
            'scale.penalty': self.scale_penalty,
            'null.space.penalty': self.null_space_penalty,
            'sparse.cons': self.sparse_cons,
            'diagonal.penalty': self.diagonal_penalty,
            'apply.by': self.apply_by,
            'modCon': self.modCon,
            'knots': self.knots,
            'n': n
        }
        
        # Filtering out None values if any parameter is not set
        r_args = {k: v for k, v in r_args.items() if v is not None}

        # Evaluate the obj string as an R expression to convert it into a smooth specification object
        r_obj = robjects.r(f'eval(parse(text="{obj}"))')

        self.smooth_con_obj = mgcv.smoothCon(obj=r_obj, data=r_data, **r_args)[0]
        return self

    def transform(self, data, n=None):
        """
        Apply the SmoothCon transformation to new data.
        
        Parameters:
        data : new data frame, model frame or list with covariate values.
        n : number of values for each covariate (if data is a list).
        """
        if self.smooth_con_obj is None:
            raise RuntimeError("The model has not been fitted yet!")
        
        if isinstance(data, pd.DataFrame):
            with localconverter(robjects.default_converter + pandas2ri.converter):
                r_data = robjects.conversion.py2rpy(data)
        else:
            raise TypeError("Data must be a pandas DataFrame")
        
        if n is None:
            n = data.shape[0]

        return mgcv.PredictMat(object=self.smooth_con_obj, data=r_data, n=n)

    def fit_transform(self, obj, data, n=None):
        """
        Fit the model and transform the data in one step.
        """
        self.fit(obj, data, n)
        return self.transform(data, n)
        
    def get_anything(self, what):
        """
        General method to retrieve any element from the smooth_con_obj based on the specified key.
        
        Parameters:
        what : str, key to access the desired element in the smooth_con_obj R list.
        
        Returns:
        The requested element from the R list object.
        """
        if self.smooth_con_obj is None:
            raise ValueError("The model has not been fitted yet!")
        return self.smooth_con_obj.rx2(what)

    def get_design(self):
        """
        Retrieve the design matrix (X) from the smooth_con_obj.
        
        Returns:
        Design matrix as a numpy array.
        """
        r_matrix = self.get_anything('X')
        return np.array(r_matrix)

    def get_penalty(self):
        """
        Retrieve the penalty matrix (S) from the smooth_con_obj.
        
        Returns:
        Penalty matrices as a list of numoy arrays.
        """
        r_list = self.get_anything('S')
        python_list = [np.array(x) for x in r_list]
        return python_list

