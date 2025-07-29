#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

__all__ = ["Classifier"]


class Classifier:
    def __init__(self):
        self.__model = None
        self.__labels = None
        self.__accuarcy = None

    def __to_dataframe(self, data):
        """
        데이터를 DataFrame 형태로 변환합니다.
        
        Parameters:
            data (dict): {"rock": [[...], [...]], "paper": [[...], ...], "scissors": [...]} 형식의 데이터
        
        Returns:
            pd.DataFrame: 데이터셋의 각 샘플을 행으로 가지는 DataFrame, label 열 포함
        """
        rows = []
        for label, samples in data.items():
            for sample in samples:
                # 각 샘플에 레이블을 추가하여 행을 생성
                rows.append(sample + [label])
        
        # DataFrame 생성: 마지막 열을 'label'로 명명
        df = pd.DataFrame(rows)
        df.columns = [f"feature_{i}" for i in range(df.shape[1] - 1)] + ["label"]
        return df

    def fit(self, data):
        """
        data 데이터의 형태는 딕셔너리 
        {"rock": [], "paper": [], "scissors":[]}
        """
        # 학습 시킬때 마다 새로운 객체 만들기 
        self.__model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.__labels = list(data.keys())
        df = self.__to_dataframe(data)

        # 특징과 레이블 분리
        X = df.drop(columns=["label"])  # 특징 데이터
        y = df["label"]  # 레이블 데이터

        # # 학습 및 테스트 데이터 분리
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.__num_columns = df.shape[1]

        # 모델 생성 및 학습
        self.__model.fit(X, y)
        self.__accuarcy = accuracy_score(y, self.__model.predict(X))

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
        return self.__accuarcy

    def save_model(self, filename):
        joblib.dump(self.__model, filename)

    def load_model(self, filename):
        self.__model = joblib.load(filename)
