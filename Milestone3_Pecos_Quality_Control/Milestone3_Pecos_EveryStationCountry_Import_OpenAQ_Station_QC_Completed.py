# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 13:32:40 2020

@author: wegia
"""


import openaq

import pandas as pd

from pandas.io.json import json_normalize

import matplotlib.pyplot as plt

from datetime import datetime, date, time, timezone

import pecos


df_DF = [];


def Milestone3_Get_Import_OpenAQ_EveryStation_inChoosenCountry(OpenAQ_StationCountry):

    
   result1 = api.cities(country=OpenAQ_StationCountry, df=True, limit=10000)
    
 #  print(result1)
    
   for index, res1 in result1.iterrows():
       
  #    print(res1['city']) 
          
      result = api.locations(city=res1['city'], df=True)

  #    print(result.dtypes)         
         
      for index1, res2 in result.iterrows():
             
     #     print(res2)
             
          df_DF.append(res2['location'])
       
     
#   df_7_DF = pd.DataFrame(df_DF)

  # print(len(df_7_DF))
#   print(df_DF)

   return df_DF  




def Milestone3_Get_Import_OpenAQ_EveryStation(OpenAQ_Countries):

   df_DF = [];

   for index, respC in OpenAQ_Countries.iterrows():
    
      df4 = respC.astype("|S")
    
       #   print(df4.dtypes)
    
   #   print(respC[0])
    
      result1 = api.cities(country=respC[0], df=True, limit=10000)
    
    #  print(result1)
    
#      result1 = api.locations(country=respC[0], df=True)

       #   print(result1)
    
      for index, res1 in result1.iterrows():
       
      #   print(res1['city']) 
          
         result = api.locations(city=res1['city'], df=True)

      #   print(result.dtypes)         
         
         for index1, res2 in result.iterrows():
             
            print(res2)
             
            df_DF.append(res2['location'])
       
     
#   df_7_DF = pd.DataFrame(df_DF)

  # print(len(df_7_DF))
   print(df_DF)

   return df_DF  

    #  print(df_2.astype("|S"))

#       df5 = pd.DataFrame(df5)
       
 #      df7 = df5.to_string()

  #     print(df7)


def Milestone3_Get_Import_OpenAQ_Countries():

   status, resp = api.cities()

   #print(resp)

   resp_attribute = api.countries(df=True)

   df2 = resp_attribute.code

   df3 = pd.DataFrame(df2)

 #  print(resp_attribute)

#   print(resp_attribute.code)

   #print(len(df3))

   return df3



def Milestone1_Get_Import_OpenAQ_Dataset_One_Staton(OpenAQStation, parameter, iterationamount):

   print(OpenAQStation)  

   Completedreq = 0
   
   # Step 1 Get Measurements for station
   try: 
     res_1 = api.measurements(location=OpenAQStation, parameter=parameter, date_to=dt_end, date_from=dt_begin, limit=10000, df=True)
     Completedreq = 1
   except:
     pass   
       
 # print(res_1.dtypes)

 # Step 2 Set utc to index 
   if(Completedreq == 1):
     OpenAQ_Dataset_ImportAPI = Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(res_1)

 # Step 3 Remove missing -999.0 measurements

     OpenAQ_Dataset_ImportAPI = Milestone2_Remove_neg_attribute(OpenAQ_Dataset_ImportAPI)

     Milestone1_Get_Measurements_OpenAQStation(OpenAQ_Dataset_ImportAPI, OpenAQStation, iterationamount)

   else: 
     OpenAQ_Dataset_ImportAPI = 0
     
  # print(OpenAQ_Dataset_ImportAPI)
 #  print(OpenAQ_Dataset_ImportAPI['value'])

#   print(OpenAQ_Dataset_ImportAPI['date.utc'])

 #  print(OpenAQ_Dataset_ImportAPI['value'])


   return OpenAQ_Dataset_ImportAPI


def Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQStation_OpenAQDataset, OpenAQStation, iteration_OpenAQStations):

   # Step 2 Initialize logger and Create a Pecos PerformanceMonitoring data object
   pecos.logger.initialize()
 
   pm = pecos.monitoring.PerformanceMonitoring()


   # Step 3 Append Dataframe to Pecos PerformanceMonitoring data object
   pm.add_dataframe(OpenAQStation_OpenAQDataset)

   # Step 4 Check the expected frequency of the timestamp
   pm.check_timestamp(900)
  
   # Step 5 Check for missing data
   pm.check_missing()
        

# Step 6 Choose acceptable value range and Check data for expected ranges
#
# Parameters
#  
#  1 Lower bound of values
#  2 Higher Bound of values
#  3 Data column (default = None, which indicates that all columns are used)
#  4 Minimum number of consecutive failures for reporting (default = 1)le increment from measurements of 15 minutes and check for abrupt changes between consecutive time steps
#
#   e.g pm.check_range([0, 200], key='value')  
#         pm.check_range([1, 2], key='3',4)
#
# Results: Any value outside of the range is an outlier

   pm.check_range([0, 200], key='value')
  
# Step 7 Choose the min amount that is acceptable to change from measurements 
#
# Parameters:
#
#    1 Lower bound to decrease by
#    2 Upper bound to increase by
#    3 Size of the moving window used to compute the difference between the minimum and maximum
#    4 Data column (default = None, which indicates that all columns are used)
#    5 Flag indicating if the test should only check for positive delta (the min occurs before the max) or negative delta (the max occurs before the min) (default = False)
#    6 Minimum number of consecutive failures for reporting (default = 1)

#  e.g. pm.check_delta([Miniumn Decrease, Min Increase], window=3600, 'value')
#      included parametes 1-6: pm.check_delta([1, 2], window=3, key='4', 5, 6)
#
#  Results: When over min decrease or increase it is an outlier


   pm.check_delta([None, 10], window=3600, key='value')

# Step 8 Choose acceptable increment on measurements 
#
# Parameters
#  
#  1 Lower bound to de increment by
#  2 Higher Bound to increment by
#  3 Data column (default = None, which indicates that all columns are used)
#  4 Increment used for difference calculation (default = 1 timestamp)
#  5 Flag indicating if the absolute value of the increment is used in the test (default = True)
#  6 Minimum number of consecutive failures for reporting (default = 1)
#
# e.g pm.check_increment([None, 20], 'value') 
#    included parametes 1- 4:  pm.check_increment([1, 2], key='3', 4, 5, 6) 
#
# Results: Any measurement that has a larger increment or de increment by choosen value is an outlier

   pm.check_increment([None, 20], key='value') 


   # Step 9 Compute the quality control index for value
   mask = pm.mask[['value']]
   QCI = pecos.metrics.qci(mask)

   custom = 'custom' + iteration_OpenAQStations + '.png'

   MeasurementOpenAQ = int(OpenAQStation_OpenAQDataset['value'].max())
   # Step 10 Generate graphics
   test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
   OpenAQStation_OpenAQDataset.plot(y='value', ylim=[1,MeasurementOpenAQ], figsize=(7.0,3.5))
   plt.savefig(custom, format='png', dpi=500)

 #  print(pm.test_results)

   # Step 11 Write test results and report files to test_results.csv and monitoringreport.html

   Report = 'test_results' + OpenAQStation + iteration_OpenAQStations + '.csv' 

   MonitoringReport = 'MonitoringReport' + OpenAQStation + iteration_OpenAQStations + '.html'

   pecos.io.write_test_results(pm.test_results,filename=Report)
   pecos.io.write_monitoring_report(pm.df, pm.test_results, test_results_graphics, 
                                 [custom], QCI,filename=MonitoringReport)

   return pm.test_results


def Milestone3_Pecos_Quality_Control_EveryStation(OpenAQ_Stations, parameter, Completed_QC_Processes):

   QC_Pecos_OpenAQ = []

 #  print(OpenAQ_Stations)
   
   iteration1 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112','113','114','115','116','117','118','119','120','121','122','123','124','125','126','127','128','129','130','131','132','133','134','135','136','137','138','139','140','141','142','143','144','145','146','147','148','149','150','151','152','153','154','155','156','157','158','159','160','161','162','163','164','165','166','167','168','169','170','171','172','173','174','175','176','177','178','179','180','181','182','183','184','185','186','187','188','189','190','191','192','193','194','195','196','197','198','199','200','201','202','203','204','205','206','207','208','209','210','211','212','213','214','215','216','217','218','219','220','221','222','223','224','225','226','227','228','229','230','231','232','233','234','235','236','237','238','239','240','241','242','243','244','245','246','247','248','249','250','251','252','253','254','255','256','257','258','259','260','261','262','263','264','265','266','267','268','269','270','271','272','273','274','275','276','277','278','279','280','281','282','283','284','285','286','287','288','289','290','291','292','293','294','295','296','297','298','299','300','301','302','303','304','305','306','307','308','309','310','311','312','313','314','315','316','317','318','319','320','321','322','323','324','325','326','327','328','329','330','331','332','333','334','335','336','337','338','339','340','341','342','343','344','345','346','347','348','349','350','351','352','353','354','355','356','357','358','359','360','361','362','363','364','365','366','367','368','369','370','371','372','373','374','375','376','377','378','379','380','381','382','383','384','385','386','387','388','389','390','391','392','393','394','395','396','397','398','399','400','401','402','403','404','405','406','407','408','409','410','411','412','413','414','415','416','417','418','419','420','421','422','423','424','425','426','427','428','429','430','431','432','433','434','435','436','437','438','439','440','441','442','443','444','445','446','447','448','449','450','451','452','453','454','455','456','457','458','459','460','461','462','463','464','465','466','467','468','469','470','471','472','473','474','475','476','477','478','479','480','481','482','483','484','485','486','487','488','489','490','491','492','493','494','495','496','497','498','499','500','501','502','503','504','505','506','507','508','509','510','511','512','513','514','515','516','517','518','519','520','521','522','523','524','525','526','527','528','529','530','531','532','533','534','535','536','537','538','539','540','541','542','543','544','545','546','547','548','549','550','551','552','553','554','555','556','557','558','559','560','561','562','563','564','565','566','567','568','569','570','571','572','573','574','575','576','577','578','579','580','581','582','583','584','585','586','587','588','589','590','591','592','593','594','595','596','597','598','599','600','601','602','603','604','605','606','607','608','609','610','611','612','613','614','615','616','617','618','619','620','621','622','623','624','625','626','627','628','629','630','631','632','633','634','635','636','637','638','639','640','641','642','643','644','645','646','647','648','649','650','651','652','653','654','655','656','657','658','659','660','661','662','663','664','665','666','667','668','669','670','671','672','673','674','675','676','677','678','679','680','681','682','683','684','685','686','687','688','689','690','691','692','693','694','695','696','697','698','699','700','701','702','703','704','705','706','707','708','709','710','711','712','713','714','715','716','717','718','719','720','721','722','723','724','725','726','727','728','729','730','731','732','733','734','735','736','737','738','739','740','741','742','743','744','745','746','747','748','749','750','751','752','753','754','755','756','757','758','759','760','761','762','763','764','765','766','767','768','769','770','771','772','773','774','775','776','777','778','779','780','781','782','783','784','785','786','787','788','789','790','791','792','793','794','795','796','797','798','799','800','801','802','803','804','805','806','807','808','809','810','811','812','813','814','815','816','817','818','819','820','821','822','823','824','825','826','827','828','829','830','831','832','833','834','835','836','837','838','839','840','841','842','843','844','845','846','847','848','849','850','851','852','853','854','855','856','857','858','859','860','861','862','863','864','865','866','867','868','869','870','871','872','873','874','875','876','877','878','879','880','881','882','883','884','885','886','887','888','889','890','891','892','893','894','895','896','897','898','899','900','901','902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924','925','926','927','928','929','930','931','932','933','934','935','936','937','938','939','940','941','942','943','944','945','946','947','948','949','950','951','952','953','954','955','956','957','958','959','960','961','962','963','964','965','966','967','968','969','970','971','972','973','974','975','976','977','978','979','980','981','982','983','984','985','986','987','988','989','990','991','992','993','994','995','996','997','998','999','1000']

   iterationamount = 0 
 
   for OpenAQStation in OpenAQ_Stations:

   #   print(OpenAQStation) 
      
      if(iterationamount >= Completed_QC_Processes):
        OpenAQStation_Dataset = Milestone1_Get_Import_OpenAQ_Dataset_One_Staton(OpenAQStation, parameter, iteration1[iterationamount])

    #    print(OpenAQStation_Dataset)
        if(OpenAQStation_Dataset != 0): 
          QC_Pecos_OpenAQ_result = Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQStation_Dataset, OpenAQStation, iteration1[iterationamount])
        else:
          QC_Pecos_OpenAQ_result = 0 
          
        QC_Pecos_OpenAQ.append(QC_Pecos_OpenAQ_result)

      iterationamount = iterationamount + 1


   return QC_Pecos_OpenAQ


def Milestone1_Get_Measurements_OpenAQStation(ResultsOpenAQ, OpenAQ_Stations, OpenAQresults):
    
   OpenAQDataset = r'D:\AirNode\Collaborations\PublicAuthority\Inter-Governmental\ECMWF\ESoWC\AQQC\Milestone3_Pecos_Quality_Control\OpenAQ_Results_station'
   
   OpenAQDataset = OpenAQDataset + OpenAQ_Stations + OpenAQresults + ".csv" 
    
   print( OpenAQDataset)
   
   ResultsOpenAQ.to_csv(OpenAQDataset,index=False)                       

   


def Milestone2_Remove_neg_attribute(OpenAQ_Dataset_ImportAPI):
    
    OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

    return OpenAQ_Dataset_ImportAPI


def Milestone2_Get_OpenAQ_Dataset_Wrangling_utc_index(OpenAQ_Dataset_ImportAPI):

   format = '%Y-%m-%d %H:%M:%S'
    
   OpenAQ_Dataset_ImportAPI['date.utc'] = pd.to_datetime(OpenAQ_Dataset_ImportAPI['date.utc'], format=format).dt.tz_localize(None)

   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI[OpenAQ_Dataset_ImportAPI.value != -999.00]

   Formating = pd.DatetimeIndex(OpenAQ_Dataset_ImportAPI['date.utc'])
                 
 
   
   OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index(Formating)

  # OpenAQ_Dataset_ImportAPI = OpenAQ_Dataset_ImportAPI.set_index('date.utc')

  # print(OpenAQ_Dataset_ImportAPI)

  # print(OpenAQ_Dataset_ImportAPI['value'])

 #  print(OpenAQ_Dataset_ImportAPI['date.utc'])


 #  print(OpenAQ_Dataset_ImportAPI['value'])

   return OpenAQ_Dataset_ImportAPI


def Test_Milestone3_Import_OpenAQ_Dataset_Station():
    
    
   res = api.latest(location='Monash', df=True)

   print(res['location'])

   return res


    
api = openaq.OpenAQ()
    


#Step 1 Choose the measurement country to import and Time Schedule
#
# 1 Choose from output of Country Codes 
#
# 2 Change country code in CountryCode
#
# res1 = api.measurements(country='IN', parameter='pm25', date_to=dt_end, date_from=dt_begin, limit=10000, df=True)
#
# 3 Test un comment   
#
# reports measurements for station
#
# result = Test_Milestone3_Import_OpenAQ_Dataset_Station()
#
# 4 Change Time Schedule from 6 months to other in dt_begin
#  and dt_end
#
#

CountryCode = 'TR'

print("Choose from ")

OpenAQ_Countries = Milestone3_Get_Import_OpenAQ_Countries()

OpenAQStations = Milestone3_Get_Import_OpenAQ_EveryStation_inChoosenCountry(CountryCode)

dt_begin = date(2020,3,1)  # Edit
dt_end = date(2020,9,1)  # Edit


print("Getting OpenAQ dataset applying pyOpenAQ API from ") 
print(dt_begin)
print(" to ")
print(dt_end)
print(" for every OpenAQ Station and parameter ")


# Step 2 Choose parameter 
#
# 1 Change parameter to pm25, pm10, no2, bc, so2, o3
#
#

parameter = 'pm25'

print(parameter)

#OpenAQ_Stations = Milestone3_Get_Import_OpenAQ_EveryStation(OpenAQ_Countries)

# Step 3 Go to Milestone3_Pecos_Complete_QualityControl_One_OpenAQStation(OpenAQStation, iteration_OpenAQStations)
#
# 1 Change Pecos Quality Control criteria 
#
#
# 

# Step 3 When OpenAQ API fails add Station failed on and retry
#
# 1 Change the variable to next number of statation after last completed 
#
# 2 Change Completed_QC_Processes 
#
# i.e. when 3 report completed change to 4 

Completed_QC_Processes = 3

QC_Pecos_OpenAQ_Results = Milestone3_Pecos_Quality_Control_EveryStation(OpenAQStations, parameter, Completed_QC_Processes)

# Step 4 Check outlier and Results
#
# 1 Open Monitoring Report
#
# 2 Check Results in OpenAQ_Results_Station + Number of Station


# Results.to_csv(r'D:\AirNode\TechnicalStack\AirNode_Dependencies\Functionality\L_IoT\Gatherminer-master\example_data\openAQ_100attr100_100.csv',index=False)                       
