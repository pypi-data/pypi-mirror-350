#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import joblib

__all__ = ["Regressor"]


class Regressor:
    def __init__(self):
        self.__model = None
        self.__target = None
        self.__mse = None
        self.coef_ = None
        self.intercept_ = None


    def __to_dataframe(self, data):
        
        # Data는 2차원 리스트이다. 
        df = pd.DataFrame(data)
        df.columns = [f"feature_{i}" for i in range(df.shape[1] - 1)] + ["target"]
        return df


    def fit(self, data):
        """
        data 데이터의 형태는 2차원 리스트이며, 타겟값은 반드시 가장 뒤에 있어야 한다. 
        lst = [[1, 2, 3], [3, 4, 5], [6, 7, 8]]
        """
        # 학습 시킬때 마다 새로운 객체 만들기 
        self.__model = LinearRegression()
        df = self.__to_dataframe(data)

        # 특징과 레이블 분리
        X = df.drop(columns=["target"])  # 특징 데이터
        y = df["target"]  # 레이블 데이터

        # # 학습 및 테스트 데이터 분리
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.__num_columns = df.shape[1]

        # 모델 생성 및 학습
        self.__model.fit(X, y)
        self.__mse = mean_squared_error(y, self.__model.predict(X))
        self.coef_ = self.__model.coef_
        self.intercept_ = self.__model.intercept_

        return self

    def __is_1d(self, lst):
        if not isinstance(lst, list):
            return 0    # 리스트 아님 
        elif len(lst) > 0 and isinstance(lst[0], list):
            return 2    # 2D
        else:
            return 1    # 1D
    
    def predict(self, data):
        d =  self.__is_1d(data)
        if d == 0:
            return 
        elif d == 1:
            data = [data]    

        # 입력을 2D로 해야한다. 
        y_pred = self.__model.predict(data)
        return y_pred

    def score(self):
        return self.__mse

    def save_model(self, filename):
        joblib.dump(self.__model, filename)

    def load_model(self, filename):
        self.__model = joblib.load(filename)