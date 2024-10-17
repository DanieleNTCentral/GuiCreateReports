import os
import re

from cryptography.x509.extensions import ExtensionTypeVar


class estraiInfo:
    def __init__(self,logging):
        self.dataEstrati = {}
        self.logging = logging
        self.logging.debug("Inizializzazione classe")


    def estrai_dati(self, listfile):
        i = 0
        typeSignal: str
        for fl in listfile:
            with open(fl, "r", encoding='utf-8') as file:
                contenuto = file.read()
                file.close()
            # Estrai valori specifici usando espressioni regolari
            match i:
                case 0:
                    typeSignal = "OS"
                case 1:
                    typeSignal = "PRS"
            print(contenuto)
            self.logging.debug("Estrazione dati da:" +fl)
            # PDOP Min e Max
            try:
                self.logging.info("Estrazione PDOP Min e Max"+ typeSignal)
                pdop_min = re.search(r'PDOPmin\s*=\s*(\d+)', contenuto)
                pdop_max = re.search(r'PDOPmax\s*=\s*(\d+)', contenuto)
                if pdop_min and pdop_max:
                    self.dataEstrati['PDOPmin' + typeSignal] = int(pdop_min.group(1))
                    self.dataEstrati['PDOPmax' + typeSignal] = int(pdop_max.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            # Estrazione dei valori TOW (Time of Week)
            try:
                self.logging.info("Estrazione Valori TOW "+ typeSignal)
                tow_iniziale = re.search(r'TOW\(s\) iniziale:\s+(\d+)', contenuto)
                tow_finale = re.search(r'TOW\(s\) finale:\s+(\d+)', contenuto)
                if tow_iniziale and tow_finale:
                    self.dataEstrati['TOW iniziale' + typeSignal] = int(tow_iniziale.group(1))
                    self.dataEstrati['TOW finale' + typeSignal] = int(tow_finale.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            # Estrazione data analisi
            try:
                self.logging.info("Estrazione dati analisi "+ typeSignal)
                analisi_iniziale = re.search(r"ora inizio analisi: (\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})", contenuto)
                analisi_finale = re.search(r"ora fine analisi: (\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})", contenuto)
                if analisi_iniziale and analisi_finale:
                    self.dataEstrati['analisi_iniziale' + typeSignal] = analisi_iniziale.group(1)
                    self.dataEstrati['analisi_finale' + typeSignal] = analisi_finale.group(1)
            except Exception as ex:
                self.logging.error("exception"+ex)
            # Numero campioni attesi e validi persi e scartati
            try:
                self.logging.info("estrazione Numero campioni attesi e validi persi e scartati "+typeSignal)
                campioni_attesi = re.search(r'Numero campioni\s+attesi:\s+(\d+)', contenuto)
                campioni_validi = re.search(r'Numero campioni\s+validi\(PVT\):\s+(\d+)', contenuto)
                campioni_persi = re.search(r'Numero campioni\s+persi\(NO PVT\):\s+(\d+)', contenuto)
                campioni_scartati = re.search(r'Numero campioni\s+scartati\s+per PDOP elevata \(PVT\):\s+(\d+)', contenuto)
                if campioni_attesi and campioni_validi and campioni_scartati and campioni_persi:
                    self.dataEstrati['Campioni attesi' + typeSignal] = int(campioni_attesi.group(1))
                    self.dataEstrati['Campioni validi' + typeSignal] = int(campioni_validi.group(1))
                    self.dataEstrati['Campioni persi' + typeSignal] = int(campioni_persi.group(1))
                    self.dataEstrati['Campioni scartati' + typeSignal] = int(campioni_scartati.group(1))
            except Exception as ex:
                self.logging.error("Excpetion"+ ex)

            # Disponibilità
            try:
                self.logging.info("Estrazione disp " +typeSignal)
                disponibility = re.search(r'Disp\(percent\):\s*([\d.]+)', contenuto)
                if disponibility:
                    self.dataEstrati['disponibility' + typeSignal] = float(disponibility.group(1))
            except Exception as ex:
                self.logging.error("Exception:" +ex)
            # PDOP
            try:
                self.logging.info("estrazione valori PDOP "+typeSignal)
                media_pdop = re.search(r'Media PDOP:\s+([\d.]+)', contenuto)
                if media_pdop:
                    self.dataEstrati['Media PDOP' + typeSignal] = float(media_pdop.group(1))
                min_pdop = re.search(r'Min PDOP:\s+([\d.]+)', contenuto)
                if min_pdop:
                    self.dataEstrati['Min PDOP' + typeSignal] = float(min_pdop.group(1))
                max_pdop = re.search(r'Max PDOP:\s+([\d.]+)', contenuto)
                if max_pdop:
                    self.dataEstrati['Max PDOP' + typeSignal] = float(max_pdop.group(1))
            except Exception as ex:
                self.logging.error("Excption:"+ex)

            # Informazioni su SAT
            # informazioni E1A
            try:
                self.logging.info("Estrazione informazioni E1A "+ typeSignal)
                mediaSatInvistaE1A = re.search(r'Media Sat in vista E1A:\s+([\d.]+)', contenuto)
                if mediaSatInvistaE1A:
                    self.dataEstrati['MediaSatVistaE1A' + typeSignal] = float(mediaSatInvistaE1A.group(1))
                MaxSatInVistaE1A = re.search(r'Max Sat in vista E1A:\s+([\d.]+)', contenuto)
                if MaxSatInVistaE1A:
                    self.dataEstrati['MaxSatInVistaE1A' + typeSignal] = float(MaxSatInVistaE1A.group(1))
                MinSatInVistaE1A = re.search(r'Min Sat in vista E1A:\s+([\d.]+)', contenuto)
                if MinSatInVistaE1A:
                    self.dataEstrati['MinSatInVistaE1A' + typeSignal] = float(MinSatInVistaE1A.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            # Informazioni E6A
            try:
                self.logging.info("Estrazione informazioni E6A "+typeSignal)
                mediaSatInvistaE6A = re.search(r'Media Sat in vista E6A:\s+([\d.]+)', contenuto)
                if mediaSatInvistaE6A:
                    self.dataEstrati['MediaSatVistaE6A' + typeSignal] = float(mediaSatInvistaE6A.group(1))
                MaxSatInVistaE6A = re.search(r'Max Sat in vista E6A:\s+([\d.]+)', contenuto)
                if MaxSatInVistaE6A:
                    self.dataEstrati['MaxSatInVistaE6A' + typeSignal] = float(MaxSatInVistaE6A.group(1))
                MinSatInVistaE6A = re.search(r'Min Sat in vista E6A:\s+([\d.]+)', contenuto)
                if MinSatInVistaE6A:
                    self.dataEstrati['MinSatInVistaE6A' + typeSignal] = float(MinSatInVistaE6A.group(1))
            except Exception as ex:
                self.logging.info("Exception:"+ex)
            # Informazioni E1BC
            try:
                self.logging.info("Estrazione informazioni E1BC "+typeSignal)
                mediaSatInvistaE1BC = re.search(r'Media Sat in vista E1BC:\s+([\d.]+)', contenuto)
                if mediaSatInvistaE1BC:
                    self.dataEstrati['MediaSatVistaE1BC' + typeSignal] = float(mediaSatInvistaE1BC.group(1))
                MaxSatInVistaE1BC = re.search(r'Max Sat in vista E1BC:\s+([\d.]+)', contenuto)
                if MaxSatInVistaE1BC:
                    self.dataEstrati['MaxSatInVistaE1BC' + typeSignal] = float(MaxSatInVistaE1BC.group(1))
                MinSatInVistaE1BC = re.search(r'Min Sat in vista E1BC:\s+([\d.]+)', contenuto)
                if MinSatInVistaE1BC:
                    self.dataEstrati['MinSatInVistaE1BC' + typeSignal] = float(MinSatInVistaE1BC.group(1))
            except Exception as ex:
                self.logging.error("Exception" +ex)
        # region HorizontalPosition
            #region Percentile 2D filtrata da PDOP
            try:
                self.logging.info("Estrazione percentile 2D filtrata da PDOP "+typeSignal)
                percentile_2d = re.search(r'Percentile 2D filtrata da PDOP:\s+([\d.]+)', contenuto)
                if percentile_2d:
                    self.dataEstrati['Percentile 2DPDOP' + typeSignal] =float(percentile_2d.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            #endregion Percentile 2D filtrata da PDOP
            #region BIAS
            try:
                self.logging.info("Estraziuone BIAS "+typeSignal)
                bias = re.search(r'bias 2D filtrata da PDOP:\s+([\d.]+)', contenuto)
                if bias:
                    self.dataEstrati['bias2D' + typeSignal] = float(bias.group(1))
            except Exception as ex:
                self.logging.erro("Exception:"+ex)
            #endregion BIAS
            #region Media errore 2D filtrata da PDOP
            try:
                self.logging.info("Media errore 2D filtrata da PDOP "+typeSignal)
                media_errore_2d = re.search(r'Media errore 2D filtrata da PDOP:\s+([\d.]+)', contenuto)
                if media_errore_2d:
                    self.dataEstrati['Media errore 2D' + typeSignal] = float(media_errore_2d.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            #endregion Media errore 2D filtrata da PDOP
            #region varianza errore 2D
            try:
                self.logging.info("estrazione varianza errore 2d "+typeSignal)
                varianza_errore_2d = re.search(r'Varianza errore 2D filtrata da PDOP:\s+([\d]+)', contenuto)
                if varianza_errore_2d:
                    self.dataEstrati['varianza errore 2D' + typeSignal] = float(varianza_errore_2d.group(1))
            except Exception as ex:
                self.logging.error("Exeption:"+ex)
            #endregion varianza errore 2D
            #region Deviazione standard errore 2D filtrata da PDOP
            try:
                self.logging.info("estrazione Deviazione standard errore 2D filtrata da PDOP "+typeSignal)
                deviazione_errore_2d = re.search(r'Deviazione standard errore 2D filtrata da PDOP:\s+([\d]+)', contenuto)
                if deviazione_errore_2d:
                    self.dataEstrati['deviazione errore 2d' + typeSignal] = float(varianza_errore_2d.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            #endregion Deviazione standard errore 2D filtrata da PDOP
            #region 3D
            # Percentile 3D filtrata da PDOP
            try:
                self.logging.info("Estrazione Percentile 3D filtrata da PDOP "+typeSignal)
                percentile_3d = re.search(r'Percentile 3D filtrata da PDOP:\s+([\d.]+)', contenuto)
                if percentile_3d:
                    self.dataEstrati['Percentile 3D' + typeSignal] = float(percentile_3d.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            # BIAS
            try:
                self.logging.info("Estrazione BIAS 3D " +typeSignal)
                bias3D = re.search(r'bias 3D\s:\s+([\d.]+)', contenuto)
                if bias:
                    self.dataEstrati['bias 3D' + typeSignal] = float(bias3D.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            # Media errore 3D filtrata da PDOP
            try:
                self.logging.info("Estrazione Media errore 3D filtrata da PDOP")
                media_errore_3d = re.search(r'Media errore 3D filtrata da PDOP:\s+([\d.]+)', contenuto)
                if media_errore_3d:
                    self.dataEstrati['Media errore 3D' + typeSignal] = float(media_errore_3d.group(1))
            except Exception as ex:
                self.logging.error("Exception:" + ex)
            # varianza errore 3D
            try:
                self.logging.info("varianza errore 3D "+typeSignal)
                varianza_errore_3d = re.search(r'Varianza errore 3D filtrata da PDOP:\s+([\d]+)', contenuto)
                if varianza_errore_3d:
                    self.dataEstrati['varianza errore 3D' + typeSignal] = float(varianza_errore_3d.group(1))
            except Exception as ex:
                self.logging.error("Exception:" + ex)
            # Deviazione standard errore 3D filtrata da PDOP
            try:
                self.logging.info("Estrazione deviazione standard errore 3d filtrara da PDOP "+typeSignal)
                deviazione_errore_3d = re.search(r'Deviazione standard errore 3D filtrata da PDOP:\s+([\d]+)', contenuto)
                if deviazione_errore_3d:
                    self.dataEstrati['deviazione errore 3d' + typeSignal] = float(varianza_errore_3d.group(1))
            except Exception as ex:
                self.logging.error("Exception:" + ex)
            #endregion 3D
        # endregion HorizontalPosition

        # region VerticalPosition
            # region Percentile 2D filtrata da PDOP
            try:
                self.logging.info("Estrazione Vertical Percentile 2D filtrata da PDOP")
                percentile_2d = re.search(r'Percentile H:\s+([\d.]+)', contenuto)
                if percentile_2d:
                    self.dataEstrati['Percentile H' + typeSignal] = float(percentile_2d.group(1))
            except Exception as ex:
                self.logging.error("Exception:" + ex)
            #endregion Percentile 2D filtrata da PDOP
            # region BIAS
            try:
                self.logging.info("Estrazione Vertical bias")
                bias = re.search(r'bias H:\s+([\d.]+)', contenuto)
                if bias:
                    self.dataEstrati['bias H' + typeSignal] = float(bias.group(1))
            except Exception as ex:
                self.logging.error("Exception:" +ex)
            #endregion BIAS
            # region Media errore 2D filtrata da PDOP
            try:
                self.logging.info("Estrazione vertical media errore 2d filtrara da PDOP "+typeSignal)
                media_errore_2d = re.search(r'Media errore H filtrata da PDOP:\s+([\d.]+)', contenuto)
                if media_errore_2d:
                    self.dataEstrati['Media errore H' + typeSignal] = float(media_errore_2d.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            #endregion Media errore 2D filtrata da PDOP
            # region varianza errore 2D
            try:
                self.logging.info("Estrazione vertical varianza errore 2d "+typeSignal)
                varianza_errore_2d = re.search(r'Varianza errore H filtrata da PDOP:\s+([\d.]+)', contenuto)
                if varianza_errore_2d:
                    self.dataEstrati['varianza errore 2D' + typeSignal] = float(varianza_errore_2d.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            #endregion varianza errore 2D
            #region Deviazione standard errore 2D filtrata da PDOP
            try:
                self.logging.info("Estrazione Vertical Deviazione standard errore 2D filtrata da PDOP "+typeSignal)
                deviazione_errore_2d = re.search(r'Deviazione standard errore H filtrata da PDOP::\s+([\d.]+)',
                                                 contenuto)
                if deviazione_errore_2d:
                    self.dataEstrati['deviazione errore 2d' + typeSignal] = float(varianza_errore_2d.group(1))
            except Exception as ex:
                self.logging.error("Exception:"+ex)
            #endregion Deviazione standard errore 2D filtrata da PDOP
        # endregion VerticalPosition
            i += 1

        return self.dataEstrati

    def pulisci_listaNome(listacompletadirectory):
        listapulita = []
        for stringa in listacompletadirectory:
            stringa_pulita = stringa.rsplit('_', 1)[0]
            # if stringa.endswith("_OS"):
            #    stringa_pulita=stringa[:-3]
            # elif stringa.endswith("_PRS"):
            #    stringa_pulita = stringa[:-4]

            if stringa_pulita not in listapulita:  # Controlla se la stringa è già presente
                listapulita.append(stringa_pulita)
        return listapulita

    def recupera_Tutti_file_risultati_Test_Nmea(singleresultNmeaFile, nomeRepo):
        resultNmeaFiles = []
        for root, dirs, files in os.walk(nomeRepo):
            if singleresultNmeaFile in files:
                resultNmeaFiles.append(os.path.join(root, singleresultNmeaFile))
        return resultNmeaFiles

    def recupera_tutte_le_immagini(self, nomeRepo, lista_immagini_da_ricercare_SatAv: list):
        result_imgae_finded_satellite_Available = []
        for root, dirs, files in os.walk(nomeRepo):
            for immagine_da_caricare in lista_immagini_da_ricercare_SatAv:
                if immagine_da_caricare in files:
                    result_imgae_finded_satellite_Available.append(os.path.join(root, immagine_da_caricare))
        return result_imgae_finded_satellite_Available

    def TOWsToDateTime(self, TOW):
        week = {'0': 'sunday', '1': 'monday', '2': 'tuesday',
                '3': 'wednesday', '4': 'thursday', '5': 'friday', '6': 'saturday'}
        secinday = 86400
        for i in range(0, 7, 1):
            if TOW >= i * secinday and TOW < (i + 1) * secinday:
                daynum = str(i)
                hour, secrest = divmod(TOW - i * secinday, 3600)
                minute, second = divmod(secrest, 60)
                break
            else:
                continue
        day = week[daynum]
        return day, hour, minute ,second
