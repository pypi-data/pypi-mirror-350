def groupfitur(spark,dataframe):
  from pyspark.sql import SparkSession
  from pyspark.sql import functions as F
  from pyspark.sql.types import *
  from pyspark.sql.window import Window as W

  kamus_auxtrc = spark.read.csv("/tmp/production/analytics/kpt/transmode_kep.csv",header=True,sep=';')

  kamus_group = kamus_auxtrc.select("auxtrc","transmode").distinct().withColumn("group", F.when(F.col("transmode").isin("PBK","TKDN","TMDN","TKLN","TMLN"),F.lit("Transfer")).otherwise(F.col("transmode")))

  kamus_group = kamus_group.filter("group in ('Transfer','TARIK','SETOR')").withColumn(
      "group_auxtrc",
      F.when(F.col("group") == "TARIK", F.lit("Tarik"))
      .when(F.col("group") == "SETOR", F.lit("Setor"))
      .otherwise(F.col("group"))).select("auxtrc","group_auxtrc").distinct()

  mutrek_esb = dataframe\
              .filter("trim(tlbds1) like 'ESB%'")\
              .withColumn("truser", F.trim(F.col("truser")))\
              .withColumn("fiturid",F.substring(F.split(F.col("tlbds1"),':')[2],-3,3))\
              .withColumn(
              "Group",
              F.when((F.col("trdorc")=='D') & (F.col("tlbds1").rlike("ESB")),
                  F.when(F.trim(F.col("fiturid")).isin(["00P", "PLN", "01C", "00W", "03C", 
                                                        "02C", "00T", "KSL", "02P", "MIT", 
                                                        "01P", "ARJ", "05P", "FIN", "GOP", 
                                                        "00C", "00I", "SYB", "AYO", "04P", 
                                                        "RTS", "PEA", "03P", "00E", "06P", 
                                                        "00G", "MPN", "ECM", "BPJ", "TPD", 
                                                        "PIC", "KAI", "OKB", "PBB","UND",
                                                        "PGD","PL3","OJK"]), "Purchase / Payment")
                  .when(F.col("fiturid").isin(["00F", "02F", "06F", "04F","00K"]), F.when(F.col("amt").isin(2500,4000,6500),"Admin Transfer").otherwise("Transfer"))
                  .when(F.col("fiturid").isin(["00W", "04W", "06W", "02W","00W"]), "Tarik Tunai")
                  .when(F.col("fiturid") == "00D", "Transaksi Perantara")
                  .when(F.col("fiturid") == "00R", "Admin?")
                  .otherwise(F.lit(None))              
                )
          ).drop("fiturid")

  mutrek_non_esb = dataframe\
                  .filter("tlbds1 not like 'ESB:%' and cifno_nasabah not like 'Z00%'")\
                  .withColumn("truser", F.trim(F.col("truser")))\
                  .withColumn("Group", F.when((F.col("auxtrc").isin(["9996","9988","1822"])) |
                                              ((F.col("auxtrc").isin(["2501","9992"])) & (F.substring(F.col("trremk"),1,6).isin(["522184","601301","532659","189512"])))
                                              , "Tarik Tunai")\
                                        .when((F.substring(F.col("tlbds2"),1,9) == "TRF PRIMA") | 
                                              (F.substring(F.col("tlbds2"),1,8) == "TRF LINK") |
                                              (F.substring(F.col("tlbds2"),1,11) == "TRF BERSAMA") |
                                              (F.substring(F.col("trremk"),1,4) == 'ATM ') |
                                              (F.substring(F.col("trremk"),1,4) == 'FROM') |
                                              (F.trim(F.col("trremk")).like("EDC%TO%")) |
                                              (F.trim(F.col("trremk")).like("%#TRFHMB")) |
                                              (F.trim(F.col("trremk")).like("%#TRFLA")) |
                                              (F.trim(F.col("trremk")).like("ATMSTRPRM%")) |
                                              (F.trim(F.col("trremk")).like("ATMLTRPRM%")) |
                                              (((F.col("auxtrc") == '8714') | (F.col("auxtrc") == '8713')) & (F.col("trremk").like("%#%")))
                                              , F.when(F.col("amt").isin(6500), "Admin Transfer").otherwise("Transfer"))
                                        .when(((F.trim(F.col("trremk")).like("FIF%"))) |
                                              (F.trim(F.col("trremk")).like("FNS%")) |
                                              (F.trim(F.col("trremk")).like("OTO%")) |
                                              (F.trim(F.col("trremk")).like("HALO%")) |
                                              (F.trim(F.col("trremk")).like("MATRIX%")) |
                                              (F.trim(F.col("trremk")).like("PUL-IM3%")) |
                                              (F.trim(F.col("trremk")).like("PROXL%")) |
                                              (F.trim(F.col("trremk")).like("AXIS%")) |
                                              (F.trim(F.col("trremk")).like("BAF%")) |
                                              (F.trim(F.col("trremk")).like("KAI%")) |
                                              (F.trim(F.col("trremk")).like("BRIVA%")) |
                                              (F.trim(F.col("trremk")).like("PUL-SIM%")) |
                                              (F.trim(F.col("trremk")).like("SMRTF%")) |
                                              (F.trim(F.col("trremk")).like("THREE%")) |
                                              (F.trim(F.col("trremk")).like("BAF%")) |
                                              (F.trim(F.col("trremk")).like("PRCH%")) |
                                              (F.trim(F.col("trremk")).like("TOPU%")) |
                                              (F.trim(F.col("trremk")).like("TOPD%")) |
                                              (F.trim(F.col("trremk")).like("PRTT%")) |
                                              ((F.trim(F.col("trremk")).like("DARI%KE%")) & (F.substring(F.col("trremk"),-3,1) == "1"))
                                              , "Purchase / Payment")).filter("group is not null")

  mutrek_non_esb_null = mutrek_non_esb.filter("group is null").join(kamus_group,["auxtrc"],"left").withColumn("group", F.coalesce(F.col("group"),F.col("group_auxtrc"))).drop("group_auxtrc")

  df_all = mutrek_esb.unionByName(mutrek_non_esb).unionByName(mutrek_non_esb_null)
  
  return df_all