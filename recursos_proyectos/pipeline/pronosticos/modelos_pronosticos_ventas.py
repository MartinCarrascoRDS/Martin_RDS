import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pmdarima.arima import auto_arima
from xgboost import XGBRegressor
from prophet import Prophet
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping


class ModelosPronosticoVentas:
    def __init__(
        self,
        df,
        columnas_grupo,
        carpeta_graficos,
        seller=None,
        fecha_inicio_train=None,
        fecha_fin_train=None,
        fecha_inicio_test=None,
        fecha_fin_test=None,
        n_lags=3
    ):
        self.df = df.copy()
        self.columnas_grupo = columnas_grupo
        self.carpeta_graficos = carpeta_graficos
        self.seller = seller
        self.fecha_inicio_train = pd.to_datetime(fecha_inicio_train)
        self.fecha_fin_train = pd.to_datetime(fecha_fin_train)
        self.fecha_inicio_test = pd.to_datetime(fecha_inicio_test)
        self.fecha_fin_test = pd.to_datetime(fecha_fin_test)
        self.n_lags = n_lags

        self.num_meses_train = self._contar_meses(self.fecha_inicio_train, self.fecha_fin_train)
        self.num_meses_test = self._contar_meses(self.fecha_inicio_test, self.fecha_fin_test)

        os.makedirs(self.carpeta_graficos, exist_ok=True)
        self.df["Fecha_Compra"] = pd.to_datetime(self.df["Fecha_Compra"])

    def _contar_meses(self, inicio, fin):
        return (fin.year - inicio.year) * 12 + (fin.month - inicio.month + 1)

    def _crear_lags(self, df, columnas_grupo, n_lags):
        df = df.sort_values('Fecha_Compra').copy()
        for lag in range(1, n_lags + 1):
            df[f'lag_{lag}'] = df.groupby(columnas_grupo)['Unidades_Vendidas'].shift(lag)
        return df

    def _limpiar_nombre_archivo(self, nombre):
        nombre = nombre.replace(' ', '_').replace('/', '_').replace('\\', '_')
        return nombre

    def _graficar_y_guardar(self, df_filtro, df_test, y_pred, mae, rmse, nombre_archivo):
        fechas_pronostico = df_test["Fecha_Compra"].values

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df_filtro["Fecha_Compra"], df_filtro["Unidades_Vendidas"], label="Datos Reales", marker="o")
        ax.plot(fechas_pronostico, y_pred, label="Pronóstico", marker="x", linestyle="--", color="orange")
        ax.set_title(f'{nombre_archivo} | MAE: {mae:.1f} | RMSE: {rmse:.1f}')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Unidades vendidas')
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate()

        nombre_archivo = self._limpiar_nombre_archivo(nombre_archivo)
        fig.tight_layout()
        fig.savefig(os.path.join(self.carpeta_graficos, f"{nombre_archivo}.png"))
        plt.close(fig)

    def ejecutar_auto_arima(self):
        resultados = []
        predicciones = []

        grupos = self.df[self.columnas_grupo].drop_duplicates()

        for _, grupo in grupos.iterrows():
            filtro = (self.df[self.columnas_grupo] == grupo.values).all(axis=1)
            df_filtro = self.df[filtro].sort_values("Fecha_Compra")

            df_train = df_filtro[
                (df_filtro["Fecha_Compra"] >= self.fecha_inicio_train) &
                (df_filtro["Fecha_Compra"] <= self.fecha_fin_train)
            ]
            df_test = df_filtro[
                (df_filtro["Fecha_Compra"] >= self.fecha_inicio_test) &
                (df_filtro["Fecha_Compra"] <= self.fecha_fin_test)
            ]

            if (
                len(df_train) < self.num_meses_train or
                len(df_test) < self.num_meses_test or
                df_train["Unidades_Vendidas"].sum() == 0 or
                df_test["Unidades_Vendidas"].sum() == 0
            ):
                continue

            try:
                y_train = df_train["Unidades_Vendidas"].values
                y_test = df_test["Unidades_Vendidas"].values

                modelo = auto_arima(
                    y_train,
                    seasonal=False,
                    trace=False,
                    error_action="ignore",
                    suppress_warnings=True
                )

                y_pred = modelo.predict(n_periods=len(df_test))

                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))

                nombre_archivo = "-".join(str(grupo[col]) for col in self.columnas_grupo)
                if self.seller:
                    nombre_archivo += f"_{self.seller}"
                nombre_archivo = self._limpiar_nombre_archivo(nombre_archivo)

                self._graficar_y_guardar(df_filtro, df_test, y_pred, mae, rmse, nombre_archivo)

                resultados.append({**grupo.to_dict(), "MAE": mae, "RMSE": rmse})
                predicciones.append({**grupo.to_dict(), "Fecha": df_test["Fecha_Compra"].values,
                                     "y_real": y_test, "y_pred": y_pred})

            except Exception as e:
                print(f"Error con grupo {grupo.to_dict()}: {e}")
                continue

        return pd.DataFrame(resultados), pd.DataFrame(predicciones)

    def ejecutar_xgboost(self):
        resultados = []
        predicciones = []

        grupos = self.df[self.columnas_grupo].drop_duplicates()

        for _, grupo in grupos.iterrows():
            filtro = (self.df[self.columnas_grupo] == grupo.values).all(axis=1)
            df_filtro = self.df[filtro].sort_values("Fecha_Compra")

            df_lags = self._crear_lags(df_filtro, self.columnas_grupo, self.n_lags)
            df_lags = df_lags.dropna()

            df_train = df_lags[
                (df_lags["Fecha_Compra"] >= self.fecha_inicio_train) &
                (df_lags["Fecha_Compra"] <= self.fecha_fin_train)
            ]
            df_test = df_lags[
                (df_lags["Fecha_Compra"] >= self.fecha_inicio_test) &
                (df_lags["Fecha_Compra"] <= self.fecha_fin_test)
            ]

            if (
                len(df_train) < self.num_meses_train or
                len(df_test) < self.num_meses_test or
                df_train["Unidades_Vendidas"].sum() == 0 or
                df_test["Unidades_Vendidas"].sum() == 0
            ):
                continue

            try:
                X_train = df_train[[f"lag_{i}" for i in range(1, self.n_lags + 1)]].values
                y_train = df_train["Unidades_Vendidas"].values
                X_test = df_test[[f"lag_{i}" for i in range(1, self.n_lags + 1)]].values
                y_test = df_test["Unidades_Vendidas"].values

                modelo = XGBRegressor(objective="reg:squarederror")
                modelo.fit(X_train, y_train)
                y_pred = modelo.predict(X_test)

                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))

                nombre_archivo = "-".join(str(grupo[col]) for col in self.columnas_grupo)
                if self.seller:
                    nombre_archivo += f"_{self.seller}"
                nombre_archivo = self._limpiar_nombre_archivo(nombre_archivo)

                self._graficar_y_guardar(df_filtro, df_test, y_pred, mae, rmse, nombre_archivo)

                resultados.append({**grupo.to_dict(), "MAE": mae, "RMSE": rmse})
                predicciones.append({**grupo.to_dict(), "Fecha": df_test["Fecha_Compra"].values,
                                     "y_real": y_test, "y_pred": y_pred})

            except Exception as e:
                print(f"Error con grupo {grupo.to_dict()}: {e}")
                continue

        return pd.DataFrame(resultados), pd.DataFrame(predicciones)

    def ejecutar_prophet(self):
        resultados = []
        predicciones = []

        grupos = self.df[self.columnas_grupo].drop_duplicates()

        for _, grupo in grupos.iterrows():
            filtro = (self.df[self.columnas_grupo] == grupo.values).all(axis=1)
            df_filtro = self.df[filtro].sort_values("Fecha_Compra")

            df_train = df_filtro[
                (df_filtro["Fecha_Compra"] >= self.fecha_inicio_train) &
                (df_filtro["Fecha_Compra"] <= self.fecha_fin_train)
            ]
            df_test = df_filtro[
                (df_filtro["Fecha_Compra"] >= self.fecha_inicio_test) &
                (df_filtro["Fecha_Compra"] <= self.fecha_fin_test)
            ]

            if (
                len(df_train) < self.num_meses_train or
                len(df_test) < self.num_meses_test or
                df_train["Unidades_Vendidas"].sum() == 0 or
                df_test["Unidades_Vendidas"].sum() == 0
            ):
                continue

            try:
                df_train_prophet = df_train.rename(columns={"Fecha_Compra": "ds", "Unidades_Vendidas": "y"})
                m = Prophet()
                m.fit(df_train_prophet)

                future = m.make_future_dataframe(periods=len(df_test), freq='M')
                forecast = m.predict(future)

                y_pred = forecast.iloc[-len(df_test):]["yhat"].values
                y_test = df_test["Unidades_Vendidas"].values

                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))

                nombre_archivo = "-".join(str(grupo[col]) for col in self.columnas_grupo)
                if self.seller:
                    nombre_archivo += f"_{self.seller}"
                nombre_archivo = self._limpiar_nombre_archivo(nombre_archivo)

                self._graficar_y_guardar(df_filtro, df_test, y_pred, mae, rmse, nombre_archivo)

                resultados.append({**grupo.to_dict(), "MAE": mae, "RMSE": rmse})
                predicciones.append({**grupo.to_dict(), "Fecha": df_test["Fecha_Compra"].values,
                                     "y_real": y_test, "y_pred": y_pred})

            except Exception as e:
                print(f"Error con grupo {grupo.to_dict()}: {e}")
                continue

        return pd.DataFrame(resultados), pd.DataFrame(predicciones)

    def ejecutar_red_neuronal(
        self,
        num_phases=3,
        epochs=200,
        use_dropout=False,
        dropout_rate=0.2,
        use_batchnorm=False
    ):
        resultados = []
        predicciones = []

        grupos = self.df[self.columnas_grupo].drop_duplicates()

        for _, grupo in grupos.iterrows():
            filtro = (self.df[self.columnas_grupo] == grupo.values).all(axis=1)
            df_filtro = self.df[filtro].sort_values("Fecha_Compra")

            df_lags = self._crear_lags(df_filtro, self.columnas_grupo, self.n_lags)
            df_lags = df_lags.dropna()

            df_train = df_lags[
                (df_lags["Fecha_Compra"] >= self.fecha_inicio_train) &
                (df_lags["Fecha_Compra"] <= self.fecha_fin_train)
            ]
            df_test = df_lags[
                (df_lags["Fecha_Compra"] >= self.fecha_inicio_test) &
                (df_lags["Fecha_Compra"] <= self.fecha_fin_test)
            ]

            if (
                len(df_train) < self.num_meses_train or
                len(df_test) < self.num_meses_test or
                df_train["Unidades_Vendidas"].sum() == 0 or
                df_test["Unidades_Vendidas"].sum() == 0
            ):
                continue

            try:
                X_train = df_train[[f"lag_{i}" for i in range(1, self.n_lags + 1)]].values
                y_train = df_train["Unidades_Vendidas"].values
                X_test = df_test[[f"lag_{i}" for i in range(1, self.n_lags + 1)]].values
                y_test = df_test["Unidades_Vendidas"].values

                # Crear el modelo
                model = Sequential()
                neurons = 2 ** (num_phases - 1)
                model.add(tf.keras.layers.Input(shape=(X_train.shape[1],)))

                for i in range(num_phases):
                    model.add(Dense(neurons, activation='relu'))
                    if use_batchnorm:
                        model.add(BatchNormalization())
                    if use_dropout:
                        model.add(Dropout(dropout_rate))
                    neurons = max(1, neurons // 2)

                model.add(Dense(1))

                model.compile(optimizer='adam', loss='mse')
                early_stop = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
                model.fit(X_train, y_train, epochs=epochs, verbose=0, callbacks=[early_stop])

                y_pred = model.predict(X_test).flatten()

                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))

                nombre_archivo = "-".join(str(grupo[col]) for col in self.columnas_grupo)
                if self.seller:
                    nombre_archivo += f"_{self.seller}"
                nombre_archivo = self._limpiar_nombre_archivo(nombre_archivo)

                self._graficar_y_guardar(df_filtro, df_test, y_pred, mae, rmse, nombre_archivo)

                resultados.append({**grupo.to_dict(), "MAE": mae, "RMSE": rmse})
                predicciones.append({**grupo.to_dict(), "Fecha": df_test["Fecha_Compra"].values,
                                     "y_real": y_test, "y_pred": y_pred})

            except Exception as e:
                print(f"Error con grupo {grupo.to_dict()}: {e}")
                continue

        return pd.DataFrame(resultados), pd.DataFrame(predicciones)


