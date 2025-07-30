import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO

class Object:
    def __init__(self, df):
        #initialisation 


        # Créer la colonne 'integration' et la remplir avec True si elle n'existe pas
        if 'integration' not in df.columns:
            df['integration'] = True
        # Remplacer les valeurs NaN par True
        df['integration'].fillna(True, inplace=True)

        # Sélectionner les flux à intégrer
        self.stream_list = df[df['integration'] == True].copy()  # Utilisez .copy() pour éviter le Warning

        self.rowCount = len(self.stream_list)

        # Créer la colonne 'StreamType'
        self.stream_list['StreamType'] = np.where(self.stream_list['Ti'] > self.stream_list['To'], 'HS', 'CS')

        # Créer de nouvelles colonnes pour les températures décalées
        self.stream_list['STi'] = np.where(self.stream_list['StreamType'] == 'HS',
                                                  self.stream_list['Ti'] - self.stream_list['dTmin2'],
                                                  self.stream_list['Ti'] + self.stream_list['dTmin2'])

        self.stream_list['STo'] = np.where(self.stream_list['StreamType'] == 'HS',
                                                  self.stream_list['To'] - self.stream_list['dTmin2'],
                                                  self.stream_list['To'] + self.stream_list['dTmin2'])

        self.stream_list['delta_H'] = self.stream_list['mCp'] * (self.stream_list['To'] - self.stream_list['Ti'])

         # Calculer T_shifted directement dans la classe
        T_shifted = np.concatenate([self.stream_list['STi'].values, self.stream_list['STo'].values])
        T_shifted = np.sort(np.unique(T_shifted))[::-1]
        self.df_T_shifted = pd.DataFrame({'T_shifted': T_shifted})



                # Créer le DataFrame df_intervals
        self.df_intervals = pd.DataFrame({'Tsup': T_shifted[:-1], 'Tinf': T_shifted[1:]})
        self.df_intervals['IntervalName'] = self.df_intervals['Tsup'].astype(str) + '-' + self.df_intervals['Tinf'].astype(str)

        self.decomposition_flux()
        self.surplus_deficit()
        self.composite_curve()
        self.below_above_stream()
        self.find_heat_exchange_combinations()
        self.calculate_stream_numbers()
        self.hen_stream_list()


    def decomposition_flux(self):
        # Ajouter des colonnes pour le nom du flux et la valeur de mCp à df_intervals
        self.df_intervals['StreamName'] = [[] for _ in range(len(self.df_intervals))]
        self.df_intervals['mCp'] = [[] for _ in range(len(self.df_intervals))]
        self.df_intervals['StreamType'] = [[] for _ in range(len(self.df_intervals))]  # Add this line

        #print('self.df_intervals===000=======',self.df_intervals)
        #print('self.stream_list==========',self.stream_list)
        # Parcourir chaque intervalle
        for idx, row in self.df_intervals.iterrows():

            # Parcourir chaque flux
            for i in range(self.rowCount):
                # Tester la condition spécifique (StreamType[i] == "CS")
                if (self.stream_list['StreamType'].iloc[i] == "CS") and (self.stream_list['STi'].iloc[i] < row['Tsup']) and (self.stream_list['STo'].iloc[i] > row['Tinf']):

                    # Flux dans l'intervalle
                    #self.df_intervals.at[idx, 'mCp'].append(-self.stream_list['mCp'][i])
                    #self.df_intervals.at[idx, 'StreamName'].append(self.stream_list['name'][i])
                    #self.df_intervals.at[idx, 'StreamType'].append(self.stream_list['StreamType'][i])  # Add this line
                    self.df_intervals.at[idx, 'mCp'].append(-self.stream_list['mCp'].iloc[i])
                    self.df_intervals.at[idx, 'StreamName'].append(self.stream_list['name'].iloc[i])
                    self.df_intervals.at[idx, 'StreamType'].append(self.stream_list['StreamType'].iloc[i])





                # Tester la condition spécifique (StreamType[i] == "HS")
                #elif (self.stream_list['StreamType'][i] == "HS") and (self.stream_list['STi'][i] > row['Tinf']) and (self.stream_list['STo'][i] < row['Tsup']):
                elif (self.stream_list['StreamType'].iloc[i] == "HS") and (self.stream_list['STi'].iloc[i] > row['Tinf']) and (self.stream_list['STo'].iloc[i] < row['Tsup']):
 

                    # Flux dans l'intervalle
                    #self.df_intervals.at[idx, 'mCp'].append(self.stream_list['mCp'][i])
                    self.df_intervals.at[idx, 'mCp'].append(self.stream_list['mCp'].iloc[i])
                    #self.df_intervals.at[idx, 'StreamName'].append(self.stream_list['name'][i])
                    self.df_intervals.at[idx, 'StreamName'].append(self.stream_list['name'].iloc[i])
                    #self.df_intervals.at[idx, 'StreamType'].append(self.stream_list['StreamType'][i]) 
                    self.df_intervals.at[idx, 'StreamType'].append(self.stream_list['StreamType'].iloc[i]) 


        #print('self.df_intervals====00=====',self.df_intervals)
        # Utiliser explode pour dupliquer les lignes pour chaque valeur de mCp
        self.df_intervals = self.df_intervals.explode(['StreamName', 'mCp', 'StreamType']).reset_index(drop=True)
        self.df_intervals = self.df_intervals.sort_values(by=['StreamName', 'Tsup']).reset_index(drop=True)
        self.df_intervals["delta_T"]=self.df_intervals['Tsup']-self.df_intervals['Tinf']
        self.df_intervals["delta_H"]=self.df_intervals["delta_T"]*self.df_intervals["mCp"]
        #print('self.df_intervals====0=====',self.df_intervals)


    def plot_streams_and_temperature_intervals(self, figsize=(12, 6),xticks_rotation=90):
        # Vérifier la présence des colonnes requises
        required_columns = ['StreamType', 'name', 'STi', 'STo', 'mCp', 'delta_H']
        for column in required_columns:
            if column not in self.stream_list.columns:
                raise ValueError(f"Colonne '{column}' manquante dans le DataFrame.")

        # Vérifier la non-nullité des colonnes nécessaires
        if self.stream_list[required_columns].isnull().values.any():
            raise ValueError("Le DataFrame contient des valeurs nulles dans les colonnes nécessaires.")

        # Extraire les colonnes nécessaires du DataFrame
        StreamType = self.stream_list['StreamType']
        names = self.stream_list['name']
        STi = self.stream_list['STi']
        STo = self.stream_list['STo']
        mCp = self.stream_list['mCp']
        delta_H = self.stream_list['delta_H']

        # Créer une nouvelle figure
        plt.figure(figsize=figsize)

        # Tracer les flux avec l'échelle de température décalée et la couleur en fonction du StreamType
        for i in range(len(names)):
            # Déterminer la couleur et tracer le flux
            if StreamType.iloc[i] == 'HS':
                plt.plot([names.iloc[i], names.iloc[i]], [STi.iloc[i], STo.iloc[i]], color='red', label=f'Stream {names.iloc[i]}')
                plt.annotate('', xy=(names.iloc[i], STo.iloc[i]), xytext=(names.iloc[i], STo.iloc[i] + 1),
                            arrowprops=dict(arrowstyle='->', color='red', lw=1), annotation_clip=False)
            else:
                plt.plot([names.iloc[i], names.iloc[i]], [STi.iloc[i], STo.iloc[i]], color='blue', label=f'Stream {names.iloc[i]}')
                plt.annotate('', xy=(names.iloc[i], STo.iloc[i]), xytext=(names.iloc[i], STo.iloc[i] - 1),
                            arrowprops=dict(arrowstyle='->', color='blue', lw=1), annotation_clip=False)

            # Calculer la position verticale moyenne pour l'annotation
            mid_temp = (STi.iloc[i] + STo.iloc[i]) / 2
            
            # Ajouter l'annotation avec la valeur arrondie de delta_H et "kW"
            plt.text(names.iloc[i], mid_temp, f'{round(delta_H.iloc[i])} kW', 
                    verticalalignment='center', horizontalalignment='center', fontsize=8, color='black')

        # Configurer les ticks et labels de l'axe y
        y_ticks = sorted(set(STi) | set(STo))
        plt.yticks(y_ticks)

        # Ajouter des lignes horizontales en pointillé pour chaque valeur de température
        for temp in y_ticks:
            plt.axhline(y=temp, linestyle='--', color='gray', alpha=0.7)

        # Définir les labels des axes et le titre
        plt.xlabel('Stream name')
        plt.ylabel('Shifted temperature (°C)')
        plt.title('Streams and temperature intervals')

        # Définir les labels des ticks de l'axe x avec les valeurs de mCp
        plt.xticks(range(len(names)), [f'{name}\n($mCp={{{mCp_val:.2f}}}$)' for name, mCp_val in zip(names, mCp)],
                fontsize=8, rotation=xticks_rotation)  # rotation=90 pour les mettre à la verticale

        # Ajuster la marge en bas pour que les labels des xticks soient bien visibles
        plt.subplots_adjust(bottom=0.25)  # Augmenter cette valeur pour plus d'espace (par exemple 0.25 ou plus)

        # Afficher le label de la température de pincement sur l'axe y
        plt.text(0, self.Pinch_Temperature, f'Pinch_Temperature = {self.Pinch_Temperature} °C',
                verticalalignment='bottom', horizontalalignment='left')

        # Afficher la grille
        plt.grid(True)

        # Afficher le graphique sans la légende
        plt.show()

#####################################################""""

    def surplus_deficit(self):
      #print("self.df_intervals:::::!!!!!",self.df_intervals)
      # Group by 'IntervalName' and aggregate the values
      self.df_surplus_deficit = self.df_intervals.groupby('IntervalName').agg({
          'Tsup': 'first',  # Keep the first value
          'Tinf': 'first',  # Keep the first value
          'StreamName':  lambda x: list(x),  # Keep the first value
          'mCp': 'sum',  # Sum the 'mCp' values
          'StreamType': lambda x: list(x),  # Keep the first value
          'delta_T': 'first',  # Sum the 'delta_T' values
          'delta_H': 'sum'  # Sum the 'delta_H' values
      }).reset_index()

      # Sort by 'Tsup' in descending order
      #print("self.df_surplus_deficit==0===:::::",self.df_surplus_deficit)
      self.df_surplus_deficit = self.df_surplus_deficit.sort_values(by='Tsup', ascending=False)
      #print("self.df_surplus_deficit==1===:::::",self.df_surplus_deficit)
      self.df_surplus_deficit['cumulative_delta_H'] =self.df_surplus_deficit['delta_H'].cumsum()
      
      #print("self.df_surplus_deficit['cumulative_delta_H']=======::::::::",self.df_surplus_deficit['cumulative_delta_H'] )
    
      self.Heating_duty=pd.to_numeric(self.df_surplus_deficit['cumulative_delta_H'], errors='coerce').min()
      if self.Heating_duty>= 0:
        self.Heating_duty = 0
      else:
         self.Heating_duty = abs(self.Heating_duty)



      # Créer une ligne avec la valeur 0 pour 'cumulative_delta_H'
      self.cumulative_delta_H = pd.concat([pd.Series([0], name='cumulative_delta_H'), self.df_surplus_deficit['cumulative_delta_H']], ignore_index=True)

      # Ajouter la nouvelle ligne à self.Heating_duty
      self.cumulative_delta_H = pd.DataFrame(self.Heating_duty + self.cumulative_delta_H)

      # Concaténer les deux colonnes dans un nouveau DataFrame
      self.GCC = pd.concat([self.df_T_shifted, self.cumulative_delta_H], axis=1)

      # Récupérer la valeur de cumulative_delta_H correspondante
      self.Cooling_duty = self.GCC.loc[self.GCC['T_shifted'].idxmin(), 'cumulative_delta_H']

      # Récupérer la valeur de T_shifted correspondante à cumulative_delta_H nulle
      self.Pinch_Temperature = self.GCC.loc[self.GCC[self.GCC['cumulative_delta_H'] == 0].index, 'T_shifted'].values[0]
      
    def plot_GCC(self):

      # Tracer la courbe de composition avec les axes inversés
      plt.plot(self.GCC['cumulative_delta_H'], self.GCC['T_shifted'], marker='o', label='Courbe de Composition')

      # Ajouter des étiquettes et un titre au graphe
      plt.xlabel('Net heat flow (kW)')
      plt.ylabel('Shifted temperature (°C)')
      plt.title('Grand composite curve')

      # Ajouter la grille
      plt.grid(True)

      # Trouver l'index du maximum de T_shifted
      max_index = self.GCC['T_shifted'].idxmax()

      # Afficher la valeur de Heating_duty au niveau du maximum de T_shifted
      plt.text(self.GCC['cumulative_delta_H'][max_index], self.GCC['T_shifted'][max_index], f'Heating_duty = {self.Heating_duty} kW', verticalalignment='bottom', horizontalalignment='left')

      # Trouver l'index du minimum de T_shifted
      min_index = self.GCC['T_shifted'].idxmin()

      # Afficher la valeur de Cooling_duty au niveau du minimum de T_shifted
      plt.text(self.GCC['cumulative_delta_H'][min_index], self.GCC['T_shifted'][min_index], f'Cooling_duty = {self.Cooling_duty} kW', verticalalignment='bottom', horizontalalignment='right')


      # Afficher la valeur de Pinch_Temperature sur l'axe des ordonnées
      plt.text(0, self.Pinch_Temperature, f'Pinch_Temperature = {self.Pinch_Temperature} °C', verticalalignment='bottom', horizontalalignment='left')


      # Afficher le graphe
      plt.show()

    def composite_curve(self):
      # Définition des fonctions d'agrégation pour chaque colonne
      agg_functions = {'delta_H': 'sum', 'mCp': 'sum', 'Tsup': 'last', 'Tinf': 'last', 'StreamName': lambda x: list(x)}

      # Groupement par IntervalName et StreamType avec application des fonctions d'agrégation
      composite_curve = self.df_intervals.groupby(['IntervalName', 'StreamType']).agg(agg_functions).reset_index()
      composite_curve = composite_curve.sort_values(by=['StreamType', 'Tsup'], ascending=[True, True])

      # Créer des copies des DataFrames résultants
      self.cold_composite_curve = composite_curve[composite_curve['StreamType'] == 'CS'].copy()
      self.hot_composite_curve = composite_curve[composite_curve['StreamType'] == 'HS'].copy()

      # Calcul de la somme cumulée par StreamType
      self.cold_composite_curve['delta_H'] =-1*self.cold_composite_curve['delta_H']
      self.cold_composite_curve['mCp'] =-1*self.cold_composite_curve['mCp']
      self.cold_composite_curve['cumulative_delta_H'] = self.cold_composite_curve['delta_H'].cumsum()
      self.hot_composite_curve['cumulative_delta_H'] = self.hot_composite_curve['delta_H'].cumsum()

      self.cold_stream=max(self.cold_composite_curve['cumulative_delta_H'])
      self.hot_stream=max(self.hot_composite_curve['cumulative_delta_H'])

      self.heat_recovery=self.hot_stream-self.Cooling_duty
      #self.heat_recovery=self.cold_stream-self.Heating_duty


      # Afficher le résultat
      self.cold_composite_curve
      self.hot_composite_curve


      # Création du nouveau dataframe avec une ligne supplémentaire
      hcc_data = {'T': [self.hot_composite_curve['Tinf'].min()] + self.hot_composite_curve['Tsup'].tolist(),
                  'Q': [0] + self.hot_composite_curve['cumulative_delta_H'].tolist()}



      self.df_hcc = pd.DataFrame(hcc_data)
      self.df_hcc


      # Création du nouveau dataframe avec une ligne supplémentaire
      ccc_data = {'T': [self.cold_composite_curve['Tinf'].min()] + self.cold_composite_curve['Tsup'].tolist(),
                  'Q': [0] + self.cold_composite_curve['cumulative_delta_H'].tolist()+self.Cooling_duty}

      self.df_ccc = pd.DataFrame(ccc_data)
      self.df_ccc

    def plot_composites_curves(self):
            # Assurer que les deux dataframes ont la même longueur
      length = max(len(self.df_hcc), len(self.df_ccc))
      self.df_hcc = self.df_hcc.reindex(range(length)).fillna(method='ffill')
      self.df_ccc = self.df_ccc.reindex(range(length)).fillna(method='ffill')

      # Tracer les données originales
      plt.plot(self.df_hcc['Q'], self.df_hcc['T'], label='courbe composite du flux chaud', marker='o')
      plt.plot(self.df_ccc['Q'], self.df_ccc['T'], label='courbe composite du flux froid', marker='o')

      # Déterminer les limites pour la région à remplir
      q_min_fill = max(self.df_hcc['Q'].min(), self.df_ccc['Q'].min())
      q_max_fill = min(self.df_hcc['Q'].max(), self.df_ccc['Q'].max())

      # Créer une séquence linéaire pour Q dans la zone à remplir
      q_fill = np.linspace(q_min_fill, q_max_fill, 100)

      # Créer des masques pour exclure certaines parties de la zone remplie
      mask_before_ccc = q_fill < self.df_hcc['Q'].min()
      mask_after_ccf = q_fill > self.df_ccc['Q'].max()

      # Appliquer les masques pour exclure les parties indésirables
      q_fill_masked = q_fill[~(mask_before_ccc | mask_after_ccf)]
      t_ccc_fill = np.interp(q_fill_masked, self.df_hcc['Q'], self.df_hcc['T'])
      t_ccf_fill = np.interp(q_fill_masked, self.df_ccc['Q'], self.df_ccc['T'])

      # Tracer la zone remplie avec rotation
      plt.fill_between(q_fill_masked, t_ccc_fill, t_ccf_fill, color='green', alpha=0.3)


      # Ajouter des lignes pointillées
      for index, row in self.df_hcc.iterrows():
          plt.axvline(x=row['Q'], color='gray', linestyle='--')
          plt.axhline(y=row['T'], color='gray', linestyle='--')

      for index, row in self.df_ccc.iterrows():
          plt.axvline(x=row['Q'], color='gray', linestyle='--')
          plt.axhline(y=row['T'], color='gray', linestyle='--')

      # Ajouter des étiquettes et un titre
      plt.xlabel('Heat flow (kW)')
      plt.ylabel('Shifted temperature (°C)')
      plt.title('Shifted hot and cold composite curves')
      plt.legend()  # Ajouter la légende

      # Afficher le graphique
      plt.show()


    def below_above_stream(self):
        new_rows = []

        # Division de chaque ligne en deux
        for index, row in self.stream_list.iterrows():
      
            if self.stream_list.loc[index, 'StreamType']=='HS' and self.stream_list.loc[index, 'STo']<self.Pinch_Temperature:
                row_below = row.copy()
                if self.Pinch_Temperature<=row_below['STi']:
                    row_below['STi'] = self.Pinch_Temperature
                new_rows.append(row_below)

            if self.stream_list.loc[index, 'StreamType']=='CS' and self.stream_list.loc[index, 'STi']<self.Pinch_Temperature:
                row_below = row.copy()
                if self.Pinch_Temperature<=row_below['STo']:
                   row_below['STo'] = self.Pinch_Temperature          
                new_rows.append(row_below)

##################################################################################
            if self.stream_list.loc[index, 'StreamType']=='HS' and self.stream_list.loc[index, 'STi']>self.Pinch_Temperature:
                row_above = row.copy()
                if self.Pinch_Temperature>=self.stream_list.loc[index, 'STo']:
                   row_above['STo'] = self.Pinch_Temperature
                else:
                   row_above['STo'] = self.stream_list.loc[index, 'STo']
                new_rows.append(row_above)


            if self.stream_list.loc[index, 'StreamType']=='CS' and self.stream_list.loc[index, 'STo']>self.Pinch_Temperature:
                row_above = row.copy()
                if self.Pinch_Temperature<=row_above['STo']:
                    row_above['STi'] = self.Pinch_Temperature
                    new_rows.append(row_above)
         





        

        # Création du nouveau DataFrame
        df_divided = pd.DataFrame(new_rows).sort_values(by=['id', 'STi']).reset_index(drop=True)


        for i, row in df_divided.iterrows():
            if row['StreamType'] == "CS":
                df_divided.at[i, 'Ti'] = row['STi'] + row['dTmin2']
                df_divided.at[i, 'To'] = row['STo'] + row['dTmin2']
            else:  # Pour les flux "HS"
                df_divided.at[i, 'Ti'] = row['STi'] - row['dTmin2']
                df_divided.at[i, 'To'] = row['STo'] - row['dTmin2']
        
     



        # Créer des copies indépendantes pour df_above et df_below
        self.stream_list_above = df_divided[(df_divided['STi'] >= self.Pinch_Temperature) & (df_divided['STo'] >= self.Pinch_Temperature) & (df_divided['STi'] != df_divided['STo'])].copy()
        self.stream_list_below = df_divided[(df_divided['STi'] <= self.Pinch_Temperature) & (df_divided['STo'] <= self.Pinch_Temperature) & (df_divided['STi'] != df_divided['STo'])].copy()

        # Effectuer les modifications avec .loc
        self.stream_list_above.loc[:, 'delta_H'] = self.stream_list_above['mCp'] * (self.stream_list_above['To'] - self.stream_list_above['Ti'])
        self.stream_list_below.loc[:, 'delta_H'] = self.stream_list_below['mCp'] * (self.stream_list_below['To'] - self.stream_list_below['Ti'])

#########################################################################################"



    def find_heat_exchange_combinations(self):
        # Extract hot and cold streams above pinch
        hot_streams_above = self.stream_list_above[self.stream_list_above['StreamType'] == 'HS']
        cold_streams_above = self.stream_list_above[self.stream_list_above['StreamType'] == 'CS']

        # Find all combinations where mCpH <= mCpC for above pinch
        self.combinations_above = [(hot_stream['name'], cold_stream['name'], hot_stream['id'], cold_stream['id'])
                                for _, hot_stream in hot_streams_above.iterrows()
                                for _, cold_stream in cold_streams_above.iterrows()
                                if hot_stream['mCp'] <= cold_stream['mCp']]

        # Extract hot and cold streams below pinch
        hot_streams_below = self.stream_list_below[self.stream_list_below['StreamType'] == 'HS']
        cold_streams_below = self.stream_list_below[self.stream_list_below['StreamType'] == 'CS']

        # Find all combinations where mCpHS >= mCpCS for below pinch
        self.combinations_below = [(hot_stream['name'], cold_stream['name'], hot_stream['id'], cold_stream['id'])
                                for _, hot_stream in hot_streams_below.iterrows()
                                for _, cold_stream in cold_streams_below.iterrows()
                                if hot_stream['mCp'] >= cold_stream['mCp']]

        # Create DataFrame for above pinch combinations
        self.combinations_above = pd.DataFrame(self.combinations_above, columns=['HS_name', 'CS_name', 'HS_id', 'CS_id'])
        self.combinations_above['Location'] = 'above'  # Add column for 'above'
        self.combinations_above['id'] = range(1, len(self.combinations_above) + 1)  # Assign local IDs starting from 1

        # Create DataFrame for below pinch combinations
        self.combinations_below = pd.DataFrame(self.combinations_below, columns=['HS_name', 'CS_name', 'HS_id', 'CS_id'])
        self.combinations_below['Location'] = 'below'  # Add column for 'below'
        self.combinations_below['id'] = range(len(self.combinations_above) + 1, len(self.combinations_above) + len(self.combinations_below) + 1)  # Continue IDs from where above ends

        # Combine the results into a single DataFrame
        self.df_combined = pd.concat([self.combinations_above, self.combinations_below], ignore_index=True)

        return self.df_combined




###################"For Heat Exchanger network"
    def calculate_stream_numbers(self):
        # Expressions for N_HS and N_CS
        self.N_HS = len(self.stream_list[self.stream_list['StreamType'] == 'HS'])
        self.N_CS = len(self.stream_list[self.stream_list['StreamType'] == 'CS'])
        # Determine the number of stages
        self.N_stage = max(self.N_CS, self.N_HS)
    
    def hen_stream_list(self):
        flux_chaud = self.stream_list[self.stream_list['StreamType'] == 'HS']
        flux_froid = self.stream_list[self.stream_list['StreamType'] == 'CS']
        self.TiHS = flux_chaud['Ti'].tolist()
        self.ToHS = flux_chaud['To'].tolist()
        self.TiCS = flux_froid['Ti'].tolist()
        self.ToCS = flux_froid['To'].tolist()
        self.mCpHS=flux_chaud['mCp'].tolist()
        self.mCpCS=flux_froid['mCp'].tolist()
        self.nameHS=flux_chaud['name'].tolist()
        self.nameCS=flux_froid['name'].tolist()

###############################"GHE########################################"""""
    def graphical_hen_design(self):
        # Initialiser une liste pour les échangeurs installés
        heat_exchangers = []

        # Fonction pour appliquer un échange de chaleur et modifier les flux
        def apply_heat_exchange(hot_stream_df, cold_stream_df):
            # Convertir les DataFrames en dictionnaires pour traitement
            hot_stream = hot_stream_df.iloc[0].to_dict()
            cold_stream = cold_stream_df.iloc[0].to_dict()

            # Trouver la quantité de chaleur échangée (basée sur la plus petite capacité thermique résiduelle)
            heat_exchanged = min(-hot_stream['delta_H'], cold_stream['delta_H'])
            if (-hot_stream['delta_H'])<cold_stream['delta_H']:
                if cold_stream["STo"]>self.Pinch_Temperature:
                    cold_stream["To"]=(heat_exchanged/cold_stream["mCp"])+cold_stream["Ti"]
                    cold_stream["STo"]=(heat_exchanged/cold_stream["mCp"])+cold_stream["STi"]
                    #print("============cold_stream To======================",cold_stream["To"])
                else:
                    cold_stream["Ti"]=cold_stream["To"]-(heat_exchanged/cold_stream["mCp"])
                    cold_stream["STi"]=cold_stream["STo"]-(heat_exchanged/cold_stream["mCp"])
                    #print("===========cold_stream Ti================",cold_stream["Ti"])

            # Créer un échangeur de chaleur et l'ajouter à la liste
            exchanger = {
                'HS_id': hot_stream['id'],
                'HS_name': hot_stream['name'],
                'HS_mCp': hot_stream['mCp'],
                'HS_Ti': hot_stream['Ti'],
                'HS_o': hot_stream['To'],

                'CS_id': cold_stream['id'],
                'CS_name': cold_stream['name'],
                'CS_mCp': cold_stream['mCp'],
                'CS_Ti': cold_stream['Ti'],
                'CS_To': cold_stream['To'],
                
                
                'HeatExchanged': heat_exchanged
            }
            heat_exchangers.append(exchanger)

            # Print pour voir la quantité de chaleur échangée
            #print(f"Échange de chaleur entre {hot_stream['name']} et {cold_stream['name']}")
            #print(f"Chaleur échangée : {heat_exchanged}")
            #print(f"Avant échange: delta_H Hot: {hot_stream['delta_H']}, delta_H Cold: {cold_stream['delta_H']}")

            # Mettre à jour les capacités thermiques résiduelles des flux
            hot_stream_df.loc[hot_stream_df.index[0], 'delta_H'] += heat_exchanged
            cold_stream_df.loc[cold_stream_df.index[0], 'delta_H'] -= heat_exchanged
            # mettre à jour To de cold stream
            cold_stream_df.loc[cold_stream_df.index[0], 'To'] = cold_stream['Ti'] #l'entrée de l'échangeur installé
            cold_stream_df.loc[cold_stream_df.index[0], 'STo'] = cold_stream['STi'] #l'entrée de l'échangeur installé


            # Print pour voir les flux après mise à jour
            #print(f"Après échange: delta_H Hot: {hot_stream_df['delta_H'].iloc[0]}, delta_H Cold: {cold_stream_df['delta_H'].iloc[0]}")
            df_exchangers = pd.DataFrame(heat_exchangers)
            #print("Réseau d'échangeurs de chaleur:")
            #print(df_exchangers)

            # Retourner les DataFrames modifiés
            return hot_stream_df, cold_stream_df

        # Afficher les listes de flux et les combinaisons pour vérification
        # print("Flux au-dessus du pinch:")
        # print(self.stream_list_above)
        # print("Combinaisons possibles au-dessus du pinch:")
        # print(self.combinations_above)

        #print("Flux en-dessous du pinch:")
        #print(self.stream_list_below)
        #print("Combinaisons possibles en-dessous du pinch:")
        #print(self.combinations_below)

        # Sélectionner les combinaisons au-dessus du pinch (si disponibles)
        if not self.combinations_above.empty:
            for i in range(len(self.combinations_above)):
                i_combination_above = self.combinations_above.iloc[i]
                #print(f"Combinaison au-dessus du pinch à tester: {i_combination_above}")

                # Extraire les flux chauds et froids à partir des identifiants
                hot_stream_id = i_combination_above['HS_id']
                cold_stream_id = i_combination_above['CS_id']

                #print(f"Recherche du flux chaud avec ID: {hot_stream_id}")
                #print(f"Recherche du flux froid avec ID: {cold_stream_id}")

                hot_stream_df = self.stream_list_above[self.stream_list_above['id'] == hot_stream_id]
                cold_stream_df = self.stream_list_above[self.stream_list_above['id'] == cold_stream_id]

                # Vérifier si les flux existent
                if not hot_stream_df.empty and not cold_stream_df.empty and (hot_stream_df['delta_H'].iloc[0] != 0.0 or cold_stream_df['delta_H'].iloc[0] != 0.0):
                    # Appliquer l'échange de chaleur pour cette combinaison
                    hot_stream_df, cold_stream_df = apply_heat_exchange(hot_stream_df, cold_stream_df)

                    # Mettre à jour `self.stream_list_above` après l'échange de chaleur
                    # Remplacer les flux mis à jour dans le DataFrame principal
                    self.remain_stream_list_above=self.stream_list_above
                    self.remain_stream_list_above.update(hot_stream_df)
                    self.remain_stream_list_above.update(cold_stream_df)

                    # Supprimer les flux totalement utilisés
                    threshold = 1
                    self.remain_stream_list_above = self.remain_stream_list_above[abs(self.remain_stream_list_above['delta_H']) > threshold]

                    # Afficher l'état mis à jour des flux
                
                else:
                    pass
                    #print(f"Flux pour l'indice {i} non trouvés dans la liste.")


        ###

        if not self.combinations_below.empty:
            for i in range(len(self.combinations_below)):
                i_combination_below = self.combinations_below.iloc[i]
                #print(f"Combinaison en-dessous du pinch à tester: {i_combination_below}")

                # Extraire les flux chauds et froids à partir des identifiants
                hot_stream_id = i_combination_below['HS_id']
                cold_stream_id = i_combination_below['CS_id']

                #print(f"Recherche du flux chaud avec ID: {hot_stream_id}")
                #print(f"Recherche du flux froid avec ID: {cold_stream_id}")

                hot_stream_df = self.stream_list_below[self.stream_list_below['id'] == hot_stream_id]
                cold_stream_df = self.stream_list_below[self.stream_list_below['id'] == cold_stream_id]

                # Vérifier si les flux existent
                if not hot_stream_df.empty and not cold_stream_df.empty and (hot_stream_df['delta_H'].iloc[0] != 0.0 or cold_stream_df['delta_H'].iloc[0] != 0.0):
                    # Appliquer l'échange de chaleur pour cette combinaison
                    hot_stream_df, cold_stream_df = apply_heat_exchange(hot_stream_df, cold_stream_df)

                    # Mettre à jour `self.stream_list_below` après l'échange de chaleur
                    # Remplacer les flux mis à jour dans le DataFrame principal
                    self.remain_stream_list_below= self.stream_list_below
                    self.remain_stream_list_below.update(hot_stream_df)
                    self.remain_stream_list_below.update(cold_stream_df)

                    # Supprimer les flux totalement utilisés
                    self.remain_stream_list_below = self.remain_stream_list_below[self.remain_stream_list_below['delta_H'] != 0.0]

                    # Afficher l'état mis à jour des flux

                else:
                    pass
                    #print(f"Flux pour l'indice {i} non trouvés dans la liste.")


        ###

        else:
            print("Aucune combinaison disponible au-dessus du pinch pour le moment.")
        df_exchangers = pd.DataFrame(heat_exchangers)
        # Print Redults:

        print("df_exchangers*********************:")
        print(df_exchangers)

        print(f"self.remain_stream_list_above************")
        print(self.remain_stream_list_above)

        print(f"self.remain_stream_list_below******************")
        print(self.remain_stream_list_below)
        
        

        return df_exchangers

###############################"GHE#############################################"""  
    def HeatExchangerNetwork(self,disp=False,dTmin=10.0):
        # Initialiser le modèle Gekko
        m = GEKKO(remote=False)
        # Utiliser les données extraites par HeatExchangerNetwork
        N_HS = self.N_HS
        N_CS = self.N_CS
        N_stage = self.N_stage
        TiHS = self.TiHS
        ToHS = self.ToHS
        TiCS = self.TiCS
        ToCS = self.ToCS
        mCpHS = self.mCpHS
        mCpCS = self.mCpCS
        nameHS=self.nameHS
        nameCS=self.nameCS

        # Autres paramètres
        ToCU, ToHU, TiCU, TiHU = 25, 150, 20, 200
        CCU, CHU =100, 100
        CF=100 #coût lié au nombre d'échangeur)
        U = 1.0
        B = 0.6

        #Variables:
        # Redéfinition des variables q et z comme des listes tridimensionnelles
        q = [[[m.Var(lb=0, name=f'q_{i}_{j}_{k}') for k in range(N_stage+1)] for j in range(N_CS)] for i in range(N_HS)]
        # Définition de z en tant que variable binaire
        z = [[[m.Var(lb=0, ub=1, integer=True, name=f'z_{i}_{j}_{k}') for k in range(N_stage+1)] for j in range(N_CS)] for i in range(N_HS)]
        qcu = [m.Var(lb=0, name=f'qcu_{i}') for i in range(N_HS)]
        qhu = [m.Var(lb=0, name=f'qhu_{j}') for j in range(N_CS)]

        # Températures aux étages pour les flux chauds et froids
        tHS = [[m.Var(TiHS[i], lb=ToHS[i], ub=TiHS[i], name=f'tHS_{i}_{k}') for k in range(N_stage+1)] for i in range(N_HS)]
        tCS = [[m.Var(TiCS[j], lb=TiCS[j], ub=ToCS[j], name=f'tCS_{j}_{k}') for k in range(N_stage+1)] for j in range(N_CS)]

        # Variables dt
        dtcu = [m.Var(value=0.0, lb=0.0) for i in range(N_HS)]
        dthu = [m.Var(value=0.0, lb=0.0) for j in range(N_CS)]
        dt = [[[m.Var(lb=0, name=f'dt_{i}_{j}_{k}') for k in range(N_stage+1)] for j in range(N_CS)] for i in range(N_HS)]
   
        # Contraintes pour fixer les températures d'entrée
        for i in range(N_HS):
            m.Equation(tHS[i][0] == TiHS[i])
        for j in range(N_CS):
            m.Equation(tCS[j][N_stage] == TiCS[j])

        # Définition de z en fonction de q
        for k in range(N_stage+1):
            for i in range(N_HS):
                for j in range(N_CS):
                    m.Equation(z[i][j][k] == 1 - m.if3(q[i][j][k], 1, 0))
                    #m.Equation(z[i][j][k]<1)

        for k in range(N_stage+1):
            for i in range(N_HS):
                for j in range(N_CS):
                    m.Equation(dt[i][j][k] <= (tHS[i][k] - tCS[j][k])+1000000.0*(1-z[i][j][k]))
                    m.Equation(dt[i][j][k] >=dTmin)
            

        for k in range(N_stage):
            for i in range(N_HS):
                for j in range(N_CS):
                    m.Equation(dt[i][j][k+1] <= (tHS[i][k+1] - tCS[j][k+1])+1000000.0*(1-z[i][j][k]))
                    m.Equation(dt[i][j][k] >=dTmin)

        # Bilan d'énergie à chaque étage
        for i in range(N_HS):
            for k in range(N_stage):
                m.Equation((tHS[i][k] - tHS[i][k+1]) * mCpHS[i] == sum(q[i][j][k] for j in range(N_CS)))
        for j in range(N_CS):
            for k in range(N_stage):
                m.Equation((tCS[j][k] - tCS[j][k+1]) * mCpCS[j] == sum(q[i][j][k] for i in range(N_HS)))
                

        # Bilan d'énergie global pour chaque flux
        for i in range(N_HS):
            m.Equation((TiHS[i] - ToHS[i]) * mCpHS[i] == sum(q[i][j][k] for j in range(N_CS) for k in range(N_stage+1)) + qcu[i])
        for j in range(N_CS):
            m.Equation((ToCS[j] - TiCS[j]) * mCpCS[j] == sum(q[i][j][k] for i in range(N_HS) for k in range(N_stage+1)) + qhu[j])

        # Contraintes pour les utilités froides et chaudes

        for i in range(N_HS):
            m.Equation((tHS[i][N_stage] - ToHS[i]) * mCpHS[i] == qcu[i])
        for j in range(N_CS):
            m.Equation((ToCS[j] - tCS[j][0]) * mCpCS[j] == qhu[j])



        # Fonction objectif pour minimiser la somme de qcu et qhu
        cost = sum(CCU*qcu[i] for i in range(N_HS)) + sum(CHU*qhu[j] for j in range(N_CS))-0.0*sum(CF * z[i][j][k] for i in range(N_HS) for j in range(N_CS) for k in range(1, N_stage+1))

        m.Minimize(cost)

        # Résolution
        m.solve(disp=disp)
        #m.solve(disp=True, solver='ipopt')

        #calcul de mCpHS_ijk
        mCpCS_ijk = [[[0 for k in range(N_stage)] for j in range(N_CS)] for i in range(N_HS)]
        mCpHS_ijk = [[[0 for k in range(N_stage)] for j in range(N_CS)] for i in range(N_HS)]

        for i in range(N_HS):
            for j in range(N_CS):
                for k in range(N_stage):
                    if tCS[j][k].value[0]>tCS[j][k+1].value[0]:
                        mCpCS_ijk[i][j][k]=q[i][j][k].value[0]/(tCS[j][k].value[0]-tCS[j][k+1].value[0])
                    else:
                        mCpCS_ijk[i][j][k]=0
                    
                    if tHS[i][k].value[0]>tHS[i][k+1].value[0]:
                        mCpHS_ijk[i][j][k]=q[i][j][k].value[0]/(tHS[i][k].value[0]-tHS[i][k+1].value[0])
                    else:
                        mCpHS_ijk[i][j][k]=0

                    #print(f'mCpCS_ijk[{i}][{j}][{k}]={mCpCS_ijk[i][j][k]}')
                    #print(f'mCpHS_ijk[{i}][{j}][{k}]={mCpHS_ijk[i][j][k]}')

        ############################"""""" Affichage des résultats############################

        # Créer des listes pour stocker les valeurs de q et z ainsi que les indices i, j, k
        q_values = []
        i_values = []
        j_values = []
        k_values = []
        mCpCS_values=[]
        mCpHS_values=[]
        nameCS_values=[]
        nameHS_values=[]
        TiCS_values=[]
        TiHS_values=[]
        ToCS_values=[]
        ToHS_values=[]

        for i in range(N_HS):
            for j in range(N_CS):
                for k in range(N_stage):
                    mCpCS_value=mCpCS_ijk[i][j][k]
                    mCpHS_value=mCpHS_ijk[i][j][k]
                    q_value = round(q[i][j][k].value[0],3)
                    q_values.append(q_value)
                    i_values.append(i)
                    j_values.append(j)
                    k_values.append(k)

                    mCpCS_values.append(mCpCS_value)
                    mCpHS_values.append(mCpHS_value)
                    nameCS_values.append(nameCS[j])
                    nameHS_values.append(nameHS[i])
                    ToCS_values.append(round(tCS[j][k].value[0],1))
                    TiHS_values.append(round(tHS[i][k].value[0],1))
                    
                    TiCS_values.append(round(tCS[j][k+1].value[0],1))
                    ToHS_values.append(round(tHS[i][k+1].value[0],1))
        




        # Créer un DataFrame pour q avec les valeurs et les indices i, j, k correspondants
        self.hen_results = pd.DataFrame({'stage k': k_values, 'HS name':nameHS_values, 'CS name':nameCS_values,'q(kW)': q_values,'mCpCS(kW/K)': mCpCS_values,'Ti_CS(°C)':TiCS_values,'To_CS(°C)':ToCS_values,'mCpHS(kW/K)': mCpHS_values,'Ti_HS(°C)':TiHS_values,'To_HS(°C)':ToHS_values})
                 # Créer un DataFrame pour les utilités froides (qcu) et chaudes (qhu)
        qcu_values = [round(qcu[i].value[0],3) for i in range(N_HS)]
        qhu_values = [round(qhu[j].value[0],3) for j in range(N_CS)]

        #print("\nBilan d'énergie pour les utilités froides (qcu):", qcu_total)
        #print("Bilan d'énergie pour les utilités chaudes (qhu):", qhu_total)

        self.hen_qcu = pd.DataFrame({'qcu_values': qcu_values,'nameHS':nameHS})
        self.hen_qhu = pd.DataFrame({'qhu_values': qhu_values,'nameCS':nameCS})

        # Calculer les bilans d'énergie
        self.hen_qcu_total = sum(qcu_values)
        self.hen_qhu_total = sum(qhu_values)

        ###########Supprimer les lignes vides ##################
        # Supprimer les lignes où qcu est égal à zéro
        self.hen_results = self.hen_results[self.hen_results['q(kW)'] != 0]

        # Supprimer les lignes où qcu_values est égal à zéro
        self.hen_qcu = self.hen_qcu[self.hen_qcu['qcu_values'] != 0]

        # Supprimer les lignes où qhu_values est égal à zéro
        self.hen_qhu = self.hen_qhu[self.hen_qhu['qhu_values'] != 0]



##################"print#######################"""""
        for i in range(N_HS):
            for j in range(N_CS):
                for k in range(N_stage):
                    pass
                    # print(f'Chaleur échangée q[{i}][{j}][{k}]: {q[i][j][k].value[0]}')  
                    # print(f'z[{i}][{j}][{k}]: {z[i][j][k].value[0]}')     
                    # print(f'qCS[i][j][k]: ({tCS[j][k].value[0]}-{tCS[j][k+1].value[0]})*{mCpCS[j]}={q[i][j][k].value[0]}')
                    # print(f'qHS[i][j][k]: ({tHS[i][k].value[0]}-{tHS[i][k+1].value[0]})*{mCpHS[i]}={q[i][j][k].value[0]}')

        for i in range(N_HS):
            for j in range(N_CS):
                for k in range(N_stage+1):
                    print(f'pinch dt[{i}][{j}][{k}]: {dt[i][j][k].value[0]}')



        for i in range(N_HS):
            #print(f'Températures aux étages pour le flux chaud {i}:')
            for k in range(N_stage+1):
                pass
                #print(f'tHS_{i}_{k}: {tHS[i][k].value[0]}')

        for j in range(N_CS):
            #print(f'Températures aux étages pour le flux froid {j}:')
            for k in range(N_stage+1):
                pass
                #print(f'tCS_{j}_{k}: {tCS[j][k].value[0]}')
