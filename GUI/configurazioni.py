import configparser

class configurazione:
    def __init__(self):
        self.Elenco_subfileds=[]

    def leggi_file_conf(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config

    def ritorno_elenco_config(self, settoreConfig):
        elenco=[]
        #config=configparser.ConfigParser()
        #config.read("config.ini")
        config= self.leggi_file_conf()
        for section in config:
            if settoreConfig in section:
                for name, value in config.items(section):
                    elenco.append(value)

        return elenco
#region ritorno nomeTemplate,NomeReport da Salvare,directoriNme ,file fda leggere per recuperar i dati .
    def ritorno_Configurazioni(self):
        config=self.leggi_file_conf()
        nomeTemplateFile=config.get("Template", "template_file")
        nome_report_da_Salvare=config.get("NomeReport","Report")
        nome_cartella_Nmea_results=config.get("ReportDirectoryNmea", "directoryNmea")
        nome_fileDaleggere=config.get('FileReusltNmea', 'FileNmea')
        return nomeTemplateFile,nome_report_da_Salvare,nome_cartella_Nmea_results,nome_fileDaleggere
#endregion

#region  recupero immagini in base alla cartella
    def recupera_immagini_daConfig(self,settoreConfig):
        elenco_immagini_config=[]
        config=self.leggi_file_conf()
        for section_satellite in config :
           if settoreConfig in section_satellite :
               for name ,value in config.items(section_satellite):
                   elenco_immagini_config.append(value)
        return elenco_immagini_config
#endregion
#region Threshold
    def recupera_Threshold(self) ->str:
        config = self.leggi_file_conf()
        return str(config.get("ValueThreshold", "ValueThreshold"))
#endregion

#region Loggin
    def recupera_loggin_config(self) ->list[str]:
        config= self.leggi_file_conf()
        datiLoggin={}
        datiLoggin["logginfile"]  =str(config.get("Loggin","Loggin_File"))
        datiLoggin["encoding"] = str(config.get("Loggin", "encoding"))
        datiLoggin["filemode"] = str(config.get("Loggin", "filemode"))
        datiLoggin["format"] = str(config.get("Loggin", "format"))
        datiLoggin["style"] = str(config.get("Loggin", "style"))

        return datiLoggin
#endregion Loggin