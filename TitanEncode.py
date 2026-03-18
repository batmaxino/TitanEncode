# ─────────────────────────────────────────────────────────────────────────────
# TitanEncode — HDR Video Mastering Suite
# Copyright (C) 2025  Massimo — License: GPL v3
# Requirements: Python 3.10+, PyQt6, ffmpeg, ffprobe
# Run: python3 TitanEncode.py
# ─────────────────────────────────────────────────────────────────────────────
import sys, os, subprocess, json, threading, time, re
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QTabWidget, QFormLayout, QComboBox, QDoubleSpinBox,
    QSpinBox, QLineEdit, QCheckBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QTextEdit, QPushButton, QFileDialog, QScrollArea,
    QMessageBox, QProgressBar, QMenuBar, QMenu, QDialog, QDialogButtonBox,
    QTextBrowser, QSplitter, QListWidget, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QColor, QFont, QIcon, QAction

# ─────────────────────────────────────────────────────────────────────────────
# TRADUZIONI
# ─────────────────────────────────────────────────────────────────────────────
LANGS = {
    "Italiano": {
        "app_title":        "TitanEncode — HDR Video Mastering Suite",
        "header_sub":       "HDR10 · x265 · x264 · VAAPI · NVENC · PSY-RD · DEBAND · CROPDETECT",
        "tab_video":        "📽  VIDEO",
        "tab_filters":      "🧪  FILTRI PRO",
        "tab_advanced":     "⚙️  AVANZATO x265",
        "tab_audio":        "🔊  AUDIO / SUB",
        "btn_load":         "📁  CARICA FILM",
        "btn_reset":        "🗑️  NUOVO FILM",
        "btn_start":        "🚀  AVVIA ENCODING",
        "btn_stop":         "⏹  STOP",
        "btn_choose_out":   "📁  SCEGLI",
        "lbl_output":       "📂  OUTPUT:",
        "lbl_out_default":  "— stessa cartella del film sorgente —",
        "lbl_report":       "LOG DI SISTEMA:",
        "lbl_ready":        "PRONTO",
        "lbl_done":         "✅  COMPLETATO",
        "lbl_error":        "❌  ERRORE — vedi log",
        "menu_file":        "File",
        "menu_options":     "Opzioni",
        "menu_help":        "Aiuto",
        "menu_load":        "Carica film...",
        "menu_reset":       "Nuovo film / Reset",
        "menu_exit":        "Esci",
        "menu_lang":        "Lingua",
        "menu_manual":      "Manuale",
        "menu_about":       "Informazioni",
        "reset_title":      "NUOVO FILM / RESET",
        "reset_msg":        "Vuoi resettare tutto e caricare un nuovo film?\n\n⚠️  Il file sorgente NON verrà eliminato dal disco.",
        "stop_warning":     "Encoding in corso!\nFerma prima con STOP.",
        "enc_video":        "Encoder Video:",
        "enc_quality":      "Qualità RF / CRF:",
        "enc_fps":          "Frame Rate:",
        "enc_preset":       "Preset Speed:",
        "enc_range":        "Color Range:",
        "enc_depth":        "Bit Depth:",
        "enc_maxrate":      "Max Bitrate (Peak):",
        "enc_bufsize":      "VBV Buffer Size:",
        "enc_web":          "Web Optimized (faststart + A/V Sync)",
        "enc_hdr":          "Passthrough HDR10 (master-display / MaxCLL)",
        "enc_hdrcopy":      "Copia HDR side-data SEI (solo sorgenti MP4)",
        "flt_aq":           "AQ Mode:",
        "flt_psy":          "Psy-RD (Luma):",
        "flt_psycb":        "Psy-RDO (Chroma):",
        "flt_sharp":        "Sharpen (unsharp):",
        "flt_denoise":      "Denoise hqdn3d:",
        "flt_gamma":        "Gamma:",
        "flt_sat":          "Saturazione:",
        "flt_deband":       "ATTIVA DE-BANDING (ottimizzato HDR 10-bit)",
        "flt_deband_str":   "De-band Strength:",
        "flt_crop":         "AUTO-CROP BANDE NERE (cropdetect 500 frame)",
        "flt_nlm":          "NL-Means Denoise (qualità alta, più lento)",
        "flt_yadif":        "DE-INTERLACE YADIF (solo sorgenti interlacciate)",
        "flt_scale":        "Scala Risoluzione:",
        "flt_scale_algo":   "Algoritmo Scale:",
        "adv_bframes":      "B-Frames:",
        "adv_badapt":       "B-Adapt:",
        "adv_lookahead":    "RC Lookahead:",
        "adv_deblock":      "Deblock (s:t):",
        "adv_merange":      "ME Range:",
        "adv_subme":        "SubME:",
        "adv_me":           "Motion Estimation:",
        "adv_ref":          "Ref Frames:",
        "adv_opengop":      "Open GOP",
        "adv_scenecut":     "Scenecut Threshold:",
        "adv_keyint":       "Keyint (max GOP):",
        "adv_threads":      "Threads (0=auto):",
        "adv_mdcv":         "HDR master-display:",
        "adv_cll":          "HDR max-cll:",
        "aud_col_id":       "ID",
        "aud_col_lang":     "Lingua",
        "aud_col_codec":    "Codec",
        "aud_col_ch":       "Ch",
        "aud_col_title":    "Titolo",
        "aud_col_action":   "Azione",
        "aud_col_def":    "▶ Auto-play",
        "aud_col_forced":  "🔒 Forzato",
        "aud_keep":         "Mantieni",
        "aud_convert":      "Converti →",
        "aud_remove":       "Rimuovi",
        "crop_detecting":   "🔍 Rilevamento bande nere...",
        "crop_found":       "   ✅ Crop rilevato:",
        "crop_none":        "   ℹ️  Nessun crop necessario.",
        "hdr_found_mdcv":   "   📊 master-display:",
        "hdr_found_cll":    "   💡 max-cll:",
        "file_loaded":      "✅ Caricato:",
        "file_tracks":      "   Video: {}  Audio: {}  Sottotitoli: {}  Durata: {}",
        "encoding_start":   ">>> AVVIO ENCODING",
        "encoding_cmd":     "📋 COMANDO:",
        "encoding_done":    "✅ COMPLETATO →",
        "encoding_err":     "❌ ERRORE FFmpeg (codice {})",
        "encoding_crit":    "❌ ERRORE CRITICO:",
        "file_exists":      "⚠️  Sovrascriverò:",
        "out_set":          "📂 Output →",
    },
    "English": {
        "app_title":        "TitanEncode — HDR Video Mastering Suite",
        "header_sub":       "HDR10 · x265 · x264 · VAAPI · NVENC · PSY-RD · DEBAND · CROPDETECT",
        "tab_video":        "📽  VIDEO",
        "tab_filters":      "🧪  FILTERS PRO",
        "tab_advanced":     "⚙️  ADVANCED x265",
        "tab_audio":        "🔊  AUDIO / SUB",
        "btn_load":         "📁  LOAD FILM",
        "btn_reset":        "🗑️  NEW FILM",
        "btn_start":        "🚀  START ENCODING",
        "btn_stop":         "⏹  STOP",
        "btn_choose_out":   "📁  CHOOSE",
        "lbl_output":       "📂  OUTPUT:",
        "lbl_out_default":  "— same folder as source file —",
        "lbl_report":       "SYSTEM LOG:",
        "lbl_ready":        "READY",
        "lbl_done":         "✅  COMPLETED",
        "lbl_error":        "❌  ERROR — check log",
        "menu_file":        "File",
        "menu_options":     "Options",
        "menu_help":        "Help",
        "menu_load":        "Load film...",
        "menu_reset":       "New film / Reset",
        "menu_exit":        "Exit",
        "menu_lang":        "Language",
        "menu_manual":      "Manual",
        "menu_about":       "About",
        "reset_title":      "NEW FILM / RESET",
        "reset_msg":        "Reset everything and load a new film?\n\n⚠️  The source file will NOT be deleted.",
        "stop_warning":     "Encoding in progress!\nStop it first.",
        "enc_video":        "Video Encoder:",
        "enc_quality":      "Quality RF / CRF:",
        "enc_fps":          "Frame Rate:",
        "enc_preset":       "Speed Preset:",
        "enc_range":        "Color Range:",
        "enc_depth":        "Bit Depth:",
        "enc_maxrate":      "Max Bitrate (Peak):",
        "enc_bufsize":      "VBV Buffer Size:",
        "enc_web":          "Web Optimized (faststart + A/V Sync)",
        "enc_hdr":          "HDR10 Passthrough (master-display / MaxCLL)",
        "enc_hdrcopy":      "Copy HDR SEI side-data (MP4 sources only)",
        "flt_aq":           "AQ Mode:",
        "flt_psy":          "Psy-RD (Luma):",
        "flt_psycb":        "Psy-RDO (Chroma):",
        "flt_sharp":        "Sharpen (unsharp):",
        "flt_denoise":      "Denoise hqdn3d:",
        "flt_gamma":        "Gamma:",
        "flt_sat":          "Saturation:",
        "flt_deband":       "ENABLE DE-BANDING (optimised for HDR 10-bit)",
        "flt_deband_str":   "De-band Strength:",
        "flt_crop":         "AUTO-CROP BLACK BARS (cropdetect 500 frames)",
        "flt_nlm":          "NL-Means Denoise (high quality, slower)",
        "flt_yadif":        "DE-INTERLACE YADIF (interlaced sources only)",
        "flt_scale":        "Scale Resolution:",
        "flt_scale_algo":   "Scale Algorithm:",
        "adv_bframes":      "B-Frames:",
        "adv_badapt":       "B-Adapt:",
        "adv_lookahead":    "RC Lookahead:",
        "adv_deblock":      "Deblock (s:t):",
        "adv_merange":      "ME Range:",
        "adv_subme":        "SubME:",
        "adv_me":           "Motion Estimation:",
        "adv_ref":          "Ref Frames:",
        "adv_opengop":      "Open GOP",
        "adv_scenecut":     "Scenecut Threshold:",
        "adv_keyint":       "Keyint (max GOP):",
        "adv_threads":      "Threads (0=auto):",
        "adv_mdcv":         "HDR master-display:",
        "adv_cll":          "HDR max-cll:",
        "aud_col_id":       "ID",
        "aud_col_lang":     "Language",
        "aud_col_codec":    "Codec",
        "aud_col_ch":       "Ch",
        "aud_col_title":    "Title",
        "aud_col_action":   "Action",
        "aud_col_def":    "▶ Auto-play",
        "aud_col_forced":  "🔒 Forzato",
        "aud_keep":         "Keep",
        "aud_convert":      "Convert →",
        "aud_remove":       "Remove",
        "crop_detecting":   "🔍 Detecting black bars...",
        "crop_found":       "   ✅ Crop detected:",
        "crop_none":        "   ℹ️  No crop needed.",
        "hdr_found_mdcv":   "   📊 master-display:",
        "hdr_found_cll":    "   💡 max-cll:",
        "file_loaded":      "✅ Loaded:",
        "file_tracks":      "   Video: {}  Audio: {}  Subtitles: {}  Duration: {}",
        "encoding_start":   ">>> ENCODING START",
        "encoding_cmd":     "📋 COMMAND:",
        "encoding_done":    "✅ COMPLETED →",
        "encoding_err":     "❌ FFmpeg ERROR (code {})",
        "encoding_crit":    "❌ CRITICAL ERROR:",
        "file_exists":      "⚠️  Overwriting:",
        "out_set":          "📂 Output →",
    },
    "Français": {
        "app_title":        "TitanEncode — HDR Video Mastering Suite",
        "header_sub":       "HDR10 · x265 · x264 · VAAPI · NVENC · PSY-RD · DEBAND · CROPDETECT",
        "tab_video":        "📽  VIDÉO",
        "tab_filters":      "🧪  FILTRES PRO",
        "tab_advanced":     "⚙️  AVANCÉ x265",
        "tab_audio":        "🔊  AUDIO / SOUS-TITRES",
        "btn_load":         "📁  CHARGER FILM",
        "btn_reset":        "🗑️  NOUVEAU FILM",
        "btn_start":        "🚀  LANCER ENCODAGE",
        "btn_stop":         "⏹  STOP",
        "btn_choose_out":   "📁  CHOISIR",
        "lbl_output":       "📂  SORTIE:",
        "lbl_out_default":  "— même dossier que la source —",
        "lbl_report":       "JOURNAL SYSTÈME:",
        "lbl_ready":        "PRÊT",
        "lbl_done":         "✅  TERMINÉ",
        "lbl_error":        "❌  ERREUR — voir journal",
        "menu_file":        "Fichier",
        "menu_options":     "Options",
        "menu_help":        "Aide",
        "menu_load":        "Charger film...",
        "menu_reset":       "Nouveau film / Reset",
        "menu_exit":        "Quitter",
        "menu_lang":        "Langue",
        "menu_manual":      "Manuel",
        "menu_about":       "À propos",
        "reset_title":      "NOUVEAU FILM / RESET",
        "reset_msg":        "Réinitialiser et charger un nouveau film?\n\n⚠️  Le fichier source NE sera PAS supprimé.",
        "stop_warning":     "Encodage en cours!\nArrêtez-le d'abord.",
        "enc_video":        "Encodeur vidéo:",
        "enc_quality":      "Qualité RF / CRF:",
        "enc_fps":          "Fréquence d'images:",
        "enc_preset":       "Préréglage vitesse:",
        "enc_range":        "Plage de couleurs:",
        "enc_depth":        "Profondeur de bits:",
        "enc_maxrate":      "Débit max (pic):",
        "enc_bufsize":      "Taille buffer VBV:",
        "enc_web":          "Optimisé web (faststart + sync A/V)",
        "enc_hdr":          "HDR10 passthrough (master-display / MaxCLL)",
        "enc_hdrcopy":      "Copier HDR SEI (sources MP4 uniquement)",
        "flt_aq":           "Mode AQ:",
        "flt_psy":          "Psy-RD (Luma):",
        "flt_psycb":        "Psy-RDO (Chroma):",
        "flt_sharp":        "Netteté (unsharp):",
        "flt_denoise":      "Débruitage hqdn3d:",
        "flt_gamma":        "Gamma:",
        "flt_sat":          "Saturation:",
        "flt_deband":       "ACTIVER LE DEBANDING (optimisé HDR 10-bit)",
        "flt_deband_str":   "Intensité deband:",
        "flt_crop":         "RECADRAGE AUTO (cropdetect 500 images)",
        "flt_nlm":          "Débruitage NL-Means (haute qualité, lent)",
        "flt_yadif":        "DÉSENTRELACEMENT YADIF (sources entrelacées)",
        "flt_scale":        "Redimensionner:",
        "flt_scale_algo":   "Algorithme:",
        "adv_bframes":      "B-Frames:",
        "adv_badapt":       "B-Adapt:",
        "adv_lookahead":    "RC Lookahead:",
        "adv_deblock":      "Deblock (s:t):",
        "adv_merange":      "Portée ME:",
        "adv_subme":        "SubME:",
        "adv_me":           "Estimation de mouvement:",
        "adv_ref":          "Frames de référence:",
        "adv_opengop":      "Open GOP",
        "adv_scenecut":     "Seuil scenecut:",
        "adv_keyint":       "Keyint (GOP max):",
        "adv_threads":      "Threads (0=auto):",
        "adv_mdcv":         "HDR master-display:",
        "adv_cll":          "HDR max-cll:",
        "aud_col_id":       "ID",
        "aud_col_lang":     "Langue",
        "aud_col_codec":    "Codec",
        "aud_col_ch":       "Ch",
        "aud_col_title":    "Titre",
        "aud_col_action":   "Action",
        "aud_col_def":    "▶ Auto-play",
        "aud_col_forced":  "🔒 Forzato",
        "aud_keep":         "Garder",
        "aud_convert":      "Convertir →",
        "aud_remove":       "Supprimer",
        "crop_detecting":   "🔍 Détection des bandes noires...",
        "crop_found":       "   ✅ Recadrage détecté:",
        "crop_none":        "   ℹ️  Aucun recadrage nécessaire.",
        "hdr_found_mdcv":   "   📊 master-display:",
        "hdr_found_cll":    "   💡 max-cll:",
        "file_loaded":      "✅ Chargé:",
        "file_tracks":      "   Vidéo: {}  Audio: {}  Sous-titres: {}  Durée: {}",
        "encoding_start":   ">>> DÉBUT ENCODAGE",
        "encoding_cmd":     "📋 COMMANDE:",
        "encoding_done":    "✅ TERMINÉ →",
        "encoding_err":     "❌ ERREUR FFmpeg (code {})",
        "encoding_crit":    "❌ ERREUR CRITIQUE:",
        "file_exists":      "⚠️  Remplacement:",
        "out_set":          "📂 Sortie →",
    },
    "Deutsch": {
        "app_title":        "TitanEncode — HDR Video Mastering Suite",
        "header_sub":       "HDR10 · x265 · x264 · VAAPI · NVENC · PSY-RD · DEBAND · CROPDETECT",
        "tab_video":        "📽  VIDEO",
        "tab_filters":      "🧪  FILTER PRO",
        "tab_advanced":     "⚙️  ERWEITERT x265",
        "tab_audio":        "🔊  AUDIO / UT",
        "btn_load":         "📁  FILM LADEN",
        "btn_reset":        "🗑️  NEUER FILM",
        "btn_start":        "🚀  ENCODING STARTEN",
        "btn_stop":         "⏹  STOP",
        "btn_choose_out":   "📁  WÄHLEN",
        "lbl_output":       "📂  AUSGABE:",
        "lbl_out_default":  "— gleicher Ordner wie Quelldatei —",
        "lbl_report":       "SYSTEMPROTOKOLL:",
        "lbl_ready":        "BEREIT",
        "lbl_done":         "✅  ABGESCHLOSSEN",
        "lbl_error":        "❌  FEHLER — Protokoll prüfen",
        "menu_file":        "Datei",
        "menu_options":     "Optionen",
        "menu_help":        "Hilfe",
        "menu_load":        "Film laden...",
        "menu_reset":       "Neuer Film / Reset",
        "menu_exit":        "Beenden",
        "menu_lang":        "Sprache",
        "menu_manual":      "Handbuch",
        "menu_about":       "Über",
        "reset_title":      "NEUER FILM / RESET",
        "reset_msg":        "Alles zurücksetzen und neuen Film laden?\n\n⚠️  Die Quelldatei wird NICHT gelöscht.",
        "stop_warning":     "Encoding läuft!\nBitte zuerst stoppen.",
        "enc_video":        "Video-Encoder:",
        "enc_quality":      "Qualität RF / CRF:",
        "enc_fps":          "Bildrate:",
        "enc_preset":       "Geschwindigkeits-Preset:",
        "enc_range":        "Farbbereich:",
        "enc_depth":        "Bittiefe:",
        "enc_maxrate":      "Max. Bitrate (Spitze):",
        "enc_bufsize":      "VBV-Puffergröße:",
        "enc_web":          "Web-Optimiert (faststart + A/V-Sync)",
        "enc_hdr":          "HDR10 Passthrough (master-display / MaxCLL)",
        "enc_hdrcopy":      "HDR SEI kopieren (nur MP4-Quellen)",
        "flt_aq":           "AQ-Modus:",
        "flt_psy":          "Psy-RD (Luma):",
        "flt_psycb":        "Psy-RDO (Chroma):",
        "flt_sharp":        "Schärfe (unsharp):",
        "flt_denoise":      "Rauschreduzierung hqdn3d:",
        "flt_gamma":        "Gamma:",
        "flt_sat":          "Sättigung:",
        "flt_deband":       "DEBANDING AKTIVIEREN (für HDR 10-bit optimiert)",
        "flt_deband_str":   "Deband-Stärke:",
        "flt_crop":         "AUTO-CROP SCHWARZE BALKEN (cropdetect)",
        "flt_nlm":          "NL-Means Rauschreduzierung (hohe Qualität, langsam)",
        "flt_yadif":        "DEINTERLACING YADIF (nur Interlaced-Quellen)",
        "flt_scale":        "Auflösung skalieren:",
        "flt_scale_algo":   "Skalierungsalgorithmus:",
        "adv_bframes":      "B-Frames:",
        "adv_badapt":       "B-Adapt:",
        "adv_lookahead":    "RC Lookahead:",
        "adv_deblock":      "Deblock (s:t):",
        "adv_merange":      "ME-Reichweite:",
        "adv_subme":        "SubME:",
        "adv_me":           "Bewegungsschätzung:",
        "adv_ref":          "Referenz-Frames:",
        "adv_opengop":      "Open GOP",
        "adv_scenecut":     "Szenenschnitt-Schwelle:",
        "adv_keyint":       "Keyint (max. GOP):",
        "adv_threads":      "Threads (0=auto):",
        "adv_mdcv":         "HDR master-display:",
        "adv_cll":          "HDR max-cll:",
        "aud_col_id":       "ID",
        "aud_col_lang":     "Sprache",
        "aud_col_codec":    "Codec",
        "aud_col_ch":       "Ch",
        "aud_col_title":    "Titel",
        "aud_col_action":   "Aktion",
        "aud_col_def":    "▶ Auto-play",
        "aud_col_forced":  "🔒 Forzato",
        "aud_keep":         "Behalten",
        "aud_convert":      "Konvert. →",
        "aud_remove":       "Entfernen",
        "crop_detecting":   "🔍 Schwarze Balken werden erkannt...",
        "crop_found":       "   ✅ Crop erkannt:",
        "crop_none":        "   ℹ️  Kein Crop nötig.",
        "hdr_found_mdcv":   "   📊 master-display:",
        "hdr_found_cll":    "   💡 max-cll:",
        "file_loaded":      "✅ Geladen:",
        "file_tracks":      "   Video: {}  Audio: {}  Untertitel: {}  Dauer: {}",
        "encoding_start":   ">>> ENCODING START",
        "encoding_cmd":     "📋 BEFEHL:",
        "encoding_done":    "✅ ABGESCHLOSSEN →",
        "encoding_err":     "❌ FFmpeg FEHLER (Code {})",
        "encoding_crit":    "❌ KRITISCHER FEHLER:",
        "file_exists":      "⚠️  Überschreibe:",
        "out_set":          "📂 Ausgabe →",
    },
    "Español": {
        "app_title":        "TitanEncode — HDR Video Mastering Suite",
        "header_sub":       "HDR10 · x265 · x264 · VAAPI · NVENC · PSY-RD · DEBAND · CROPDETECT",
        "tab_video":        "📽  VÍDEO",
        "tab_filters":      "🧪  FILTROS PRO",
        "tab_advanced":     "⚙️  AVANZADO x265",
        "tab_audio":        "🔊  AUDIO / SUB",
        "btn_load":         "📁  CARGAR PELÍCULA",
        "btn_reset":        "🗑️  NUEVA PELÍCULA",
        "btn_start":        "🚀  INICIAR CODIFICACIÓN",
        "btn_stop":         "⏹  STOP",
        "btn_choose_out":   "📁  ELEGIR",
        "lbl_output":       "📂  SALIDA:",
        "lbl_out_default":  "— misma carpeta que el archivo fuente —",
        "lbl_report":       "REGISTRO DEL SISTEMA:",
        "lbl_ready":        "LISTO",
        "lbl_done":         "✅  COMPLETADO",
        "lbl_error":        "❌  ERROR — ver registro",
        "menu_file":        "Archivo",
        "menu_options":     "Opciones",
        "menu_help":        "Ayuda",
        "menu_load":        "Cargar película...",
        "menu_reset":       "Nueva película / Reset",
        "menu_exit":        "Salir",
        "menu_lang":        "Idioma",
        "menu_manual":      "Manual",
        "menu_about":       "Acerca de",
        "reset_title":      "NUEVA PELÍCULA / RESET",
        "reset_msg":        "¿Resetear todo y cargar una nueva película?\n\n⚠️  El archivo fuente NO se eliminará.",
        "stop_warning":     "¡Codificación en curso!\nDetenerla primero.",
        "enc_video":        "Codificador de vídeo:",
        "enc_quality":      "Calidad RF / CRF:",
        "enc_fps":          "Fotogramas por segundo:",
        "enc_preset":       "Preset de velocidad:",
        "enc_range":        "Rango de color:",
        "enc_depth":        "Profundidad de bits:",
        "enc_maxrate":      "Bitrate máx. (pico):",
        "enc_bufsize":      "Tamaño buffer VBV:",
        "enc_web":          "Optimizado para web (faststart + sync A/V)",
        "enc_hdr":          "HDR10 passthrough (master-display / MaxCLL)",
        "enc_hdrcopy":      "Copiar SEI HDR (solo fuentes MP4)",
        "flt_aq":           "Modo AQ:",
        "flt_psy":          "Psy-RD (Luma):",
        "flt_psycb":        "Psy-RDO (Chroma):",
        "flt_sharp":        "Nitidez (unsharp):",
        "flt_denoise":      "Reducción ruido hqdn3d:",
        "flt_gamma":        "Gamma:",
        "flt_sat":          "Saturación:",
        "flt_deband":       "ACTIVAR DEBANDING (optimizado HDR 10-bit)",
        "flt_deband_str":   "Intensidad deband:",
        "flt_crop":         "RECORTE AUTOMÁTICO (cropdetect 500 frames)",
        "flt_nlm":          "Denoise NL-Means (alta calidad, lento)",
        "flt_yadif":        "DESENTRELAZADO YADIF (solo fuentes entrelazadas)",
        "flt_scale":        "Escalar resolución:",
        "flt_scale_algo":   "Algoritmo de escala:",
        "adv_bframes":      "B-Frames:",
        "adv_badapt":       "B-Adapt:",
        "adv_lookahead":    "RC Lookahead:",
        "adv_deblock":      "Deblock (f:u):",
        "adv_merange":      "Rango ME:",
        "adv_subme":        "SubME:",
        "adv_me":           "Estimación de movimiento:",
        "adv_ref":          "Frames de referencia:",
        "adv_opengop":      "Open GOP",
        "adv_scenecut":     "Umbral scenecut:",
        "adv_keyint":       "Keyint (GOP máx.):",
        "adv_threads":      "Hilos (0=auto):",
        "adv_mdcv":         "HDR master-display:",
        "adv_cll":          "HDR max-cll:",
        "aud_col_id":       "ID",
        "aud_col_lang":     "Idioma",
        "aud_col_codec":    "Codec",
        "aud_col_ch":       "Ch",
        "aud_col_title":    "Título",
        "aud_col_action":   "Acción",
        "aud_col_def":    "▶ Auto-play",
        "aud_col_forced":  "🔒 Forzato",
        "aud_keep":         "Mantener",
        "aud_convert":      "Convertir →",
        "aud_remove":       "Eliminar",
        "crop_detecting":   "🔍 Detectando barras negras...",
        "crop_found":       "   ✅ Recorte detectado:",
        "crop_none":        "   ℹ️  No se necesita recorte.",
        "hdr_found_mdcv":   "   📊 master-display:",
        "hdr_found_cll":    "   💡 max-cll:",
        "file_loaded":      "✅ Cargado:",
        "file_tracks":      "   Vídeo: {}  Audio: {}  Subtítulos: {}  Duración: {}",
        "encoding_start":   ">>> INICIO CODIFICACIÓN",
        "encoding_cmd":     "📋 COMANDO:",
        "encoding_done":    "✅ COMPLETADO →",
        "encoding_err":     "❌ ERROR FFmpeg (código {})",
        "encoding_crit":    "❌ ERROR CRÍTICO:",
        "file_exists":      "⚠️  Sobreescribiendo:",
        "out_set":          "📂 Salida →",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# STILE
# ─────────────────────────────────────────────────────────────────────────────
STYLE = """
QMainWindow, QWidget           { background: #f0f4fa; color: #1e293b; }
QMenuBar                       { background: #1e3a8a; color: #ffffff; font-size: 10pt; }
QMenuBar::item:selected        { background: #2563eb; color: #ffffff; }
QMenu                          { background: #ffffff; color: #1e293b; border: 1px solid #cbd5e1; }
QMenu::item:selected           { background: #eff6ff; color: #1d4ed8; }
QTabWidget::pane               { border: 1px solid #cbd5e1; background: #ffffff; border-radius: 6px; }
QTabBar::tab                   { background: #e2e8f0; color: #64748b; padding: 10px 24px;
                                  font-weight: bold; font-size: 10pt; border: 1px solid #cbd5e1;
                                  min-width: 110px; border-radius: 4px 4px 0 0; }
QTabBar::tab:selected          { background: #ffffff; color: #1d4ed8;
                                  border-bottom: 3px solid #2563eb; }
QTabBar::tab:hover             { background: #dbeafe; color: #1d4ed8; }
QComboBox, QDoubleSpinBox, QSpinBox, QLineEdit {
    background: #eff6ff; color: #1e293b; border: 1px solid #bfdbfe;
    border-radius: 5px; padding: 5px 10px; font-size: 10pt; }
QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
    border: 1px solid #2563eb; background: #ffffff; }
QComboBox::drop-down           { border: none; width: 20px; }
QCheckBox                      { color: #1e293b; font-size: 10pt; spacing: 10px; }
QCheckBox::indicator           { width: 20px; height: 20px; border: 2px solid #94a3b8;
                                  border-radius: 4px; background: #ffffff; }
QCheckBox::indicator:checked   { background: #ffffff; border: 2px solid #2563eb;
                                  width: 20px; height: 20px; border-radius: 4px; }
QCheckBox::indicator:hover     { border-color: #2563eb; background: #eff6ff; }
QLabel                         { color: #374151; font-size: 10pt; }
QScrollArea                    { border: none; background: #ffffff; }
QScrollBar:vertical            { background: #e2e8f0; width: 10px; border-radius: 5px; }
QScrollBar::handle:vertical    { background: #94a3b8; border-radius: 5px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #2563eb; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar:horizontal          { background: #e2e8f0; height: 10px; border-radius: 5px; }
QScrollBar::handle:horizontal  { background: #94a3b8; border-radius: 5px; min-width: 30px; }
QScrollBar::handle:horizontal:hover { background: #2563eb; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
QTableWidget                   { background: #ffffff; color: #1e293b; gridline-color: #e2e8f0;
                                  border: 1px solid #cbd5e1; border-radius: 4px; font-size: 9pt; }
QTableWidget::item             { padding: 5px 8px; }
QTableWidget::item:selected    { background: #dbeafe; color: #1d4ed8; }
QTableWidget::item:alternate   { background: #f8fafc; }
QHeaderView::section           { background: #1e3a8a; color: #ffffff; font-weight: bold;
                                  padding: 7px; border: 1px solid #1e40af; font-size: 9pt; }
QTextEdit                      { background: #1e293b; color: #7dd3fc; font-family: 'Courier New', monospace;
                                  font-size: 9pt; border: 1px solid #cbd5e1; border-radius: 4px; }
QProgressBar                   { background: #e2e8f0; border: 1px solid #bfdbfe; border-radius: 8px;
                                  height: 28px; text-align: center; color: #1e3a8a;
                                  font-weight: bold; font-size: 9pt; }
QProgressBar::chunk            { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                                  stop:0 #1d4ed8, stop:1 #3b82f6);
                                  border-radius: 7px; }
QToolTip                       { background: #1e3a8a; color: #ffffff; border: 1px solid #2563eb;
                                  border-radius: 4px; padding: 6px 10px; font-size: 9pt; }
QSplitter::handle              { background: #cbd5e1; }
"""

def btn_style(bg, fg, hover="#1d4ed8", hov_fg="#ffffff", size=11):
    return (
        f"QPushButton {{ background: {bg}; color: {fg}; font-weight: bold; font-size: {size}pt; "
        f"border-radius: 8px; padding: 6px 18px; border: none; }}"
        f"QPushButton:hover {{ background: {hover}; color: {hov_fg}; }}"
        f"QPushButton:disabled {{ background: #e2e8f0; color: #94a3b8; }}"
    )

# ─────────────────────────────────────────────────────────────────────────────
# MANUALE
# ─────────────────────────────────────────────────────────────────────────────
MANUAL_IT = {
    "Come si usa": """
<h2 style='color:#4a9eff'>Come usare TitanEncode</h2>
<h3>1. Carica il film</h3>
<p>Clicca <b>CARICA FILM</b> e scegli il file sorgente (MKV, MP4, TS, AVI, M2TS).<br>
Il programma analizzerà automaticamente le tracce audio/sottotitoli e leggerà i metadati HDR.</p>
<h3>2. Configura il video</h3>
<p>Nella scheda <b>VIDEO</b> scegli encoder, qualità RF e preset.<br>
Per archivio definitivo usa <b>libx265 + RF 20 + preset slow</b>.<br>
Per conversioni veloci usa <b>medium</b>.</p>
<h3>3. Filtri (opzionale)</h3>
<p>La scheda <b>FILTRI PRO</b> permette di applicare crop automatico, denoise, sharpen e deband.<br>
Per Blu-ray e file 4K già puliti, lascia tutto ai valori default.</p>
<h3>4. Audio</h3>
<p>Nella scheda <b>AUDIO / SUB</b> scegli per ogni traccia:<br>
- <b>Mantieni</b>: copia la traccia senza ricodifica<br>
- <b>Converti</b>: ricodifica nel formato scelto<br>
- <b>Rimuovi</b>: escludi la traccia dal file di output</p>
<h3>5. Cartella output</h3>
<p>Di default il file viene salvato nella stessa cartella del sorgente.<br>
Usa il pulsante <b>SCEGLI</b> per impostare una cartella diversa.</p>
<h3>6. Avvia</h3>
<p>Clicca <b>AVVIA ENCODING</b>. La barra mostra il progresso e il tempo rimanente.<br>
Puoi fermare la conversione in qualsiasi momento con <b>STOP</b>.</p>
<h3>7. Nuovo film</h3>
<p>Clicca <b>NUOVO FILM</b> per resettare l'interfaccia e caricare un altro file.</p>
""",
    "Requisiti software": """
<h2 style='color:#4a9eff'>Requisiti software</h2>
<h3>Obbligatori</h3>
<table border='1' cellpadding='6' style='border-color:#2a2d4a; color:#e8eaf6'>
<tr><th>Software</th><th>Versione minima</th><th>Installazione (Arch/CachyOS)</th></tr>
<tr><td><b>Python</b></td><td>3.10+</td><td>già installato</td></tr>
<tr><td><b>PyQt6</b></td><td>6.4+</td><td><code>pip install PyQt6</code></td></tr>
<tr><td><b>FFmpeg</b></td><td>5.0+</td><td><code>sudo pacman -S ffmpeg</code></td></tr>
<tr><td><b>ffprobe</b></td><td>5.0+</td><td>incluso in ffmpeg</td></tr>
</table>
<h3>Opzionali (per encoder hardware)</h3>
<table border='1' cellpadding='6' style='border-color:#2a2d4a; color:#e8eaf6'>
<tr><th>Software</th><th>Per cosa</th><th>Installazione</th></tr>
<tr><td><b>mesa-va-drivers</b></td><td>VAAPI (AMD/Intel)</td><td><code>sudo pacman -S mesa</code></td></tr>
<tr><td><b>nvidia-utils</b></td><td>NVENC (NVIDIA)</td><td><code>sudo pacman -S nvidia-utils</code></td></tr>
</table>
<h3>Avvio</h3>
<pre style='background:#0d0e1a; padding:10px; border-radius:4px; color:#a8c7fa'>python3 TitanEncode.py</pre>
""",
    "Codec spiegati": """
<h2 style='color:#4a9eff'>Codec video spiegati</h2>
<h3>libx265 (HEVC software)</h3>
<p>Il migliore per qualità e compressione. Standard per HDR10 e 4K.<br>
Lento ma produce file fino al 50% più piccoli di x264 a parità di qualità.<br>
<b>Usa questo per l'archivio definitivo.</b></p>
<h3>libx264 (AVC software)</h3>
<p>Compatibilità universale. Gira su qualsiasi dispositivo.<br>
Più veloce di x265 ma file più grandi. Non supporta HDR10 nativo.<br>
<b>Usa questo per massima compatibilità.</b></p>
<h3>hevc_vaapi (HEVC hardware AMD/Intel)</h3>
<p>Encoding hardware tramite GPU. Molto più veloce di x265 software.<br>
Qualità inferiore a parità di dimensione file.<br>
<b>Usa questo per encoding rapido quando la qualità non è prioritaria.</b></p>
<h3>hevc_nvenc (HEVC hardware NVIDIA)</h3>
<p>Come vaapi ma per schede NVIDIA. Richiede driver NVIDIA installati.<br>
<b>Usa questo se hai una GPU NVIDIA.</b></p>
<h3>RF/CRF — la qualità</h3>
<table border='1' cellpadding='6' style='border-color:#2a2d4a; color:#e8eaf6'>
<tr><th>Valore</th><th>Qualità</th><th>Uso tipico</th></tr>
<tr><td>16-18</td><td>Quasi lossless</td><td>Master definitivo</td></tr>
<tr><td>19-21</td><td>Eccellente</td><td>Archivio HDR 4K ✅</td></tr>
<tr><td>22-24</td><td>Buona</td><td>Uso quotidiano</td></tr>
<tr><td>25-28</td><td>Accettabile</td><td>Spazio limitato</td></tr>
<tr><td>29+</td><td>Scarsa</td><td>Non consigliato</td></tr>
</table>
""",
    "FAQ": """
<h2 style='color:#4a9eff'>Domande frequenti</h2>
<h3>Quanto tempo ci vuole?</h3>
<p>Dipende da CPU, preset e durata del film. Con preset <b>slow</b> su un Ryzen 4-core:<br>
- Film 2 ore → circa 1h30-2h di encoding<br>
- Film 2 ore con <b>medium</b> → circa 40-60 minuti</p>
<h3>Il file HDR perde i metadati?</h3>
<p>No. TitanEncode legge automaticamente master-display e max-cll dalla sorgente con ffprobe
e li inserisce nel file di output tramite x265. Il TV vedrà gli stessi metadati HDR dell'originale.</p>
<h3>Perché la barra progresso va a scatti?</h3>
<p>x265 non aggiorna i progressi ogni frame ma ogni secondo circa. È normale.</p>
<h3>Posso usarlo su Windows o macOS?</h3>
<p>Sì, Python e PyQt6 sono cross-platform. Assicurati che ffmpeg e ffprobe siano nel PATH.</p>
<h3>Il crop automatico è sicuro?</h3>
<p>Sì. Analizza 500 frame al centro del film per trovare le bande nere.
Se non trova bande sicure non applica nessun crop.</p>
<h3>Cosa succede se premo STOP?</h3>
<p>La conversione viene interrotta immediatamente. Il file di output parziale viene lasciato
sul disco — puoi eliminarlo manualmente.</p>
""",
}

# Manuali in tutte le lingue
MANUAL_EN = {
    "How to use": """
<h2 style='color:#1d4ed8'>How to use TitanEncode</h2>
<h3>1. Load the film</h3>
<p>Click <b>LOAD FILM</b> and choose the source file (MKV, MP4, TS, AVI, M2TS).<br>
The program will automatically analyze audio/subtitle tracks and read HDR metadata.</p>
<h3>2. Configure video</h3>
<p>In the <b>VIDEO</b> tab choose encoder, RF quality and preset.<br>
For definitive archive use <b>libx265 + RF 20 + preset slow</b>.<br>
For fast conversions use <b>medium</b>.</p>
<h3>3. Filters (optional)</h3>
<p>The <b>FILTERS PRO</b> tab allows auto-crop, denoise, sharpen and deband.<br>
For Blu-ray and clean 4K files, leave everything at default values.</p>
<h3>4. Audio</h3>
<p>In the <b>AUDIO / SUB</b> tab choose for each track:<br>
- <b>Keep</b>: copy track without re-encoding<br>
- <b>Convert</b>: re-encode to chosen format<br>
- <b>Remove</b>: exclude track from output file</p>
<h3>5. Output folder</h3>
<p>By default the file is saved in the same folder as the source.<br>
Use the <b>CHOOSE</b> button to set a different folder.</p>
<h3>6. Start</h3>
<p>Click <b>START ENCODING</b>. The bar shows progress and remaining time.<br>
You can stop the conversion at any time with <b>STOP</b>.</p>
<h3>7. New film</h3>
<p>Click <b>NEW FILM</b> to reset the interface and load another file.</p>
""",
    "Requirements": """
<h2 style='color:#1d4ed8'>Software requirements</h2>
<h3>Required</h3>
<table border='1' cellpadding='6' style='border-color:#cbd5e1; color:#1e293b'>
<tr><th>Software</th><th>Min version</th><th>Install (Arch/CachyOS)</th></tr>
<tr><td><b>Python</b></td><td>3.10+</td><td>already installed</td></tr>
<tr><td><b>PyQt6</b></td><td>6.4+</td><td><code>pip install PyQt6</code></td></tr>
<tr><td><b>FFmpeg</b></td><td>5.0+</td><td><code>sudo pacman -S ffmpeg</code></td></tr>
<tr><td><b>ffprobe</b></td><td>5.0+</td><td>included with ffmpeg</td></tr>
</table>
<h3>Optional (hardware encoders)</h3>
<table border='1' cellpadding='6' style='border-color:#cbd5e1; color:#1e293b'>
<tr><th>Software</th><th>For what</th><th>Install</th></tr>
<tr><td><b>mesa-va-drivers</b></td><td>VAAPI (AMD/Intel)</td><td><code>sudo pacman -S mesa</code></td></tr>
<tr><td><b>nvidia-utils</b></td><td>NVENC (NVIDIA)</td><td><code>sudo pacman -S nvidia-utils</code></td></tr>
</table>
<h3>Launch</h3>
<pre style='background:#1e293b; padding:10px; border-radius:4px; color:#7dd3fc'>python3 TitanEncode.py</pre>
""",
    "Codecs explained": """
<h2 style='color:#1d4ed8'>Video codecs explained</h2>
<h3>libx265 (HEVC software)</h3>
<p>Best for quality and compression. Standard for HDR10 and 4K.<br>
Slow but produces files up to 50% smaller than x264 at equal quality.<br>
<b>Use this for definitive archive.</b></p>
<h3>libx264 (AVC software)</h3>
<p>Universal compatibility. Runs on any device.<br>
Faster than x265 but larger files. No native HDR10.<br>
<b>Use this for maximum compatibility.</b></p>
<h3>hevc_vaapi (HEVC hardware AMD/Intel)</h3>
<p>Hardware encoding via GPU. Much faster than x265 software.<br>
Lower quality at same file size.<br>
<b>Use this for fast encoding when quality is not priority.</b></p>
<h3>hevc_nvenc (HEVC hardware NVIDIA)</h3>
<p>Like vaapi but for NVIDIA cards. Requires NVIDIA drivers.<br>
<b>Use this if you have a NVIDIA GPU.</b></p>
<h3>RF/CRF — quality</h3>
<table border='1' cellpadding='6' style='border-color:#cbd5e1; color:#1e293b'>
<tr><th>Value</th><th>Quality</th><th>Typical use</th></tr>
<tr><td>16-18</td><td>Near lossless</td><td>Definitive master</td></tr>
<tr><td>19-21</td><td>Excellent</td><td>HDR 4K archive ✅</td></tr>
<tr><td>22-24</td><td>Good</td><td>Daily use</td></tr>
<tr><td>25-28</td><td>Acceptable</td><td>Limited space</td></tr>
<tr><td>29+</td><td>Poor</td><td>Not recommended</td></tr>
</table>
""",
    "FAQ": """
<h2 style='color:#1d4ed8'>Frequently asked questions</h2>
<h3>How long does it take?</h3>
<p>Depends on CPU, preset and film duration. With preset <b>slow</b> on a Ryzen 4-core:<br>
- 2 hour film → about 1h30-2h encoding<br>
- 2 hour film with <b>medium</b> → about 40-60 minutes</p>
<h3>Does the HDR file lose metadata?</h3>
<p>No. TitanEncode automatically reads master-display and max-cll from the source with ffprobe
and inserts them in the output via x265. The TV will see the same HDR metadata as the original.</p>
<h3>Why does the progress bar jump?</h3>
<p>x265 does not update progress every frame but about every second. This is normal.</p>
<h3>Can I use it on Windows or macOS?</h3>
<p>Yes, Python and PyQt6 are cross-platform. Make sure ffmpeg and ffprobe are in your PATH.</p>
<h3>Is auto-crop safe?</h3>
<p>Yes. It analyzes 500 frames to find the safest crop. If no safe crop is found, nothing is applied.</p>
<h3>What happens if I press STOP?</h3>
<p>The conversion stops immediately. The partial output file is left on disk — delete it manually.</p>
""",
}

MANUAL_FR = {
    "Utilisation": """
<h2 style='color:#1d4ed8'>Comment utiliser TitanEncode</h2>
<h3>1. Charger le film</h3>
<p>Cliquez <b>CHARGER FILM</b> et choisissez le fichier source (MKV, MP4, TS, AVI, M2TS).<br>
Le programme analysera automatiquement les pistes audio/sous-titres et lira les métadonnées HDR.</p>
<h3>2. Configurer la vidéo</h3>
<p>Dans l'onglet <b>VIDÉO</b>, choisissez l'encodeur, la qualité RF et le préréglage.<br>
Pour une archive définitive : <b>libx265 + RF 20 + préréglage slow</b>.</p>
<h3>3. Filtres (optionnel)</h3>
<p>L'onglet <b>FILTRES PRO</b> permet le recadrage auto, le débruitage, la netteté et le deband.</p>
<h3>4. Audio</h3>
<p>Dans l'onglet <b>AUDIO / SOUS-TITRES</b> choisissez pour chaque piste :<br>
- <b>Garder</b> : copie sans ré-encodage<br>
- <b>Convertir</b> : ré-encode au format choisi<br>
- <b>Supprimer</b> : exclut la piste du fichier de sortie</p>
<h3>5. Dossier de sortie</h3>
<p>Par défaut le fichier est enregistré dans le même dossier que la source.<br>
Utilisez <b>CHOISIR</b> pour définir un dossier différent.</p>
<h3>6. Lancer</h3>
<p>Cliquez <b>LANCER ENCODAGE</b>. La barre montre la progression et le temps restant.</p>
""",
    "Prérequis": """
<h2 style='color:#1d4ed8'>Prérequis logiciels</h2>
<table border='1' cellpadding='6' style='border-color:#cbd5e1; color:#1e293b'>
<tr><th>Logiciel</th><th>Version min.</th><th>Installation</th></tr>
<tr><td><b>Python</b></td><td>3.10+</td><td>déjà installé</td></tr>
<tr><td><b>PyQt6</b></td><td>6.4+</td><td><code>pip install PyQt6</code></td></tr>
<tr><td><b>FFmpeg</b></td><td>5.0+</td><td><code>sudo pacman -S ffmpeg</code></td></tr>
</table>
<pre style='background:#1e293b; padding:10px; border-radius:4px; color:#7dd3fc'>python3 TitanEncode.py</pre>
""",
    "Codecs": """
<h2 style='color:#1d4ed8'>Codecs vidéo expliqués</h2>
<h3>libx265</h3><p>Meilleure qualité et compression. Standard HDR10/4K. Lent mais fichiers 50% plus petits.</p>
<h3>libx264</h3><p>Compatibilité universelle. Plus rapide mais fichiers plus grands. Pas de HDR10 natif.</p>
<h3>hevc_vaapi</h3><p>Encodage matériel GPU AMD/Intel. Très rapide, qualité inférieure.</p>
<h3>hevc_nvenc</h3><p>Comme vaapi mais pour NVIDIA.</p>
""",
    "FAQ": """
<h2 style='color:#1d4ed8'>Questions fréquentes</h2>
<h3>Combien de temps faut-il ?</h3>
<p>Avec le préréglage <b>slow</b> sur un Ryzen 4 cœurs : film 2h → environ 1h30-2h d'encodage.</p>
<h3>Le fichier HDR perd-il les métadonnées ?</h3>
<p>Non. TitanEncode lit automatiquement master-display et max-cll depuis la source et les insère via x265.</p>
<h3>Que se passe-t-il si j'appuie sur STOP ?</h3>
<p>La conversion s'arrête immédiatement. Le fichier partiel reste sur le disque.</p>
""",
}

MANUAL_DE = {
    "Verwendung": """
<h2 style='color:#1d4ed8'>TitanEncode verwenden</h2>
<h3>1. Film laden</h3>
<p>Klicken Sie <b>FILM LADEN</b> und wählen Sie die Quelldatei (MKV, MP4, TS, AVI, M2TS).<br>
Das Programm analysiert automatisch Audio-/Untertitelspuren und liest HDR-Metadaten.</p>
<h3>2. Video konfigurieren</h3>
<p>Wählen Sie im <b>VIDEO</b>-Tab Encoder, RF-Qualität und Preset.<br>
Für ein endgültiges Archiv: <b>libx265 + RF 20 + Preset slow</b>.</p>
<h3>3. Audio</h3>
<p>Im <b>AUDIO / UT</b>-Tab wählen Sie für jede Spur:<br>
- <b>Behalten</b>: kopiert ohne Neukodierung<br>
- <b>Konvertieren</b>: kodiert im gewählten Format neu<br>
- <b>Entfernen</b>: schließt Spur aus</p>
<h3>4. Starten</h3>
<p>Klicken Sie <b>ENCODING STARTEN</b>. Der Balken zeigt Fortschritt und verbleibende Zeit.</p>
""",
    "Anforderungen": """
<h2 style='color:#1d4ed8'>Softwareanforderungen</h2>
<table border='1' cellpadding='6' style='border-color:#cbd5e1; color:#1e293b'>
<tr><th>Software</th><th>Min. Version</th><th>Installation</th></tr>
<tr><td><b>Python</b></td><td>3.10+</td><td>bereits installiert</td></tr>
<tr><td><b>PyQt6</b></td><td>6.4+</td><td><code>pip install PyQt6</code></td></tr>
<tr><td><b>FFmpeg</b></td><td>5.0+</td><td><code>sudo pacman -S ffmpeg</code></td></tr>
</table>
<pre style='background:#1e293b; padding:10px; border-radius:4px; color:#7dd3fc'>python3 TitanEncode.py</pre>
""",
    "Codecs": """
<h2 style='color:#1d4ed8'>Video-Codecs erklärt</h2>
<h3>libx265</h3><p>Beste Qualität und Kompression. Standard für HDR10/4K. Langsam aber bis zu 50% kleinere Dateien.</p>
<h3>libx264</h3><p>Universelle Kompatibilität. Schneller aber größere Dateien. Kein natives HDR10.</p>
<h3>hevc_vaapi</h3><p>Hardware-Encoding über AMD/Intel GPU. Sehr schnell, geringere Qualität.</p>
<h3>hevc_nvenc</h3><p>Wie vaapi aber für NVIDIA-Karten.</p>
""",
    "FAQ": """
<h2 style='color:#1d4ed8'>Häufige Fragen</h2>
<h3>Wie lange dauert es?</h3>
<p>Mit Preset <b>slow</b> auf einem Ryzen 4-Kern: 2h Film → ca. 1h30-2h Encoding.</p>
<h3>Verliert die HDR-Datei Metadaten?</h3>
<p>Nein. TitanEncode liest master-display und max-cll automatisch aus der Quelle und fügt sie via x265 ein.</p>
<h3>Was passiert beim STOP?</h3>
<p>Die Konvertierung stoppt sofort. Die Teildatei bleibt auf der Festplatte.</p>
""",
}

MANUAL_ES = {
    "Cómo usar": """
<h2 style='color:#1d4ed8'>Cómo usar TitanEncode</h2>
<h3>1. Cargar la película</h3>
<p>Haga clic en <b>CARGAR PELÍCULA</b> y elija el archivo fuente (MKV, MP4, TS, AVI, M2TS).<br>
El programa analizará automáticamente las pistas de audio/subtítulos y leerá los metadatos HDR.</p>
<h3>2. Configurar el vídeo</h3>
<p>En la pestaña <b>VÍDEO</b> elija el codificador, calidad RF y preset.<br>
Para archivo definitivo: <b>libx265 + RF 20 + preset slow</b>.</p>
<h3>3. Audio</h3>
<p>En la pestaña <b>AUDIO / SUB</b> elija para cada pista:<br>
- <b>Mantener</b>: copia sin recodificación<br>
- <b>Convertir</b>: recodifica al formato elegido<br>
- <b>Eliminar</b>: excluye la pista del archivo de salida</p>
<h3>4. Iniciar</h3>
<p>Haga clic en <b>INICIAR CODIFICACIÓN</b>. La barra muestra el progreso y el tiempo restante.</p>
""",
    "Requisitos": """
<h2 style='color:#1d4ed8'>Requisitos de software</h2>
<table border='1' cellpadding='6' style='border-color:#cbd5e1; color:#1e293b'>
<tr><th>Software</th><th>Versión mín.</th><th>Instalación</th></tr>
<tr><td><b>Python</b></td><td>3.10+</td><td>ya instalado</td></tr>
<tr><td><b>PyQt6</b></td><td>6.4+</td><td><code>pip install PyQt6</code></td></tr>
<tr><td><b>FFmpeg</b></td><td>5.0+</td><td><code>sudo pacman -S ffmpeg</code></td></tr>
</table>
<pre style='background:#1e293b; padding:10px; border-radius:4px; color:#7dd3fc'>python3 TitanEncode.py</pre>
""",
    "Codecs": """
<h2 style='color:#1d4ed8'>Codecs de vídeo explicados</h2>
<h3>libx265</h3><p>La mejor calidad y compresión. Estándar para HDR10/4K. Lento pero archivos 50% más pequeños.</p>
<h3>libx264</h3><p>Compatibilidad universal. Más rápido pero archivos más grandes. Sin HDR10 nativo.</p>
<h3>hevc_vaapi</h3><p>Codificación hardware GPU AMD/Intel. Muy rápido, menor calidad.</p>
<h3>hevc_nvenc</h3><p>Como vaapi pero para NVIDIA.</p>
""",
    "FAQ": """
<h2 style='color:#1d4ed8'>Preguntas frecuentes</h2>
<h3>¿Cuánto tiempo tarda?</h3>
<p>Con preset <b>slow</b> en un Ryzen 4 núcleos: película 2h → unos 1h30-2h de codificación.</p>
<h3>¿El archivo HDR pierde los metadatos?</h3>
<p>No. TitanEncode lee automáticamente master-display y max-cll de la fuente y los inserta via x265.</p>
<h3>¿Qué pasa si pulso STOP?</h3>
<p>La conversión se detiene inmediatamente. El archivo parcial queda en el disco.</p>
""",
}

# Dizionario globale manuali per lingua
MANUALS = {
    "Italiano":  MANUAL_IT,
    "English":   MANUAL_EN,
    "Français":  MANUAL_FR,
    "Deutsch":   MANUAL_DE,
    "Español":   MANUAL_ES,
}

# ─────────────────────────────────────────────────────────────────────────────
# CHECKBOX CON SPUNTA VISIBILE — funziona con PyQt6 senza SVG esterni
# ─────────────────────────────────────────────────────────────────────────────
class SpuntaCheck(QCheckBox):
    """Checkbox con spunta blu visibile — tema chiaro professionale."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aggiorna_stile()
        self.stateChanged.connect(self._aggiorna_stile)

    def _aggiorna_stile(self):
        if self.isChecked():
            self.setStyleSheet(
                "QCheckBox { color: #1e293b; font-size: 10pt; spacing: 10px; }"
                "QCheckBox::indicator { width: 20px; height: 20px; background: #ffffff;"
                "  border: 2px solid #2563eb; border-radius: 4px; }"
                "QCheckBox::indicator:checked { background: #ffffff; border: 2px solid #2563eb;"
                "  width: 20px; height: 20px; }"
            )
            t = self.text()
            if not t.startswith("✔  "):
                self.setText("✔  " + t.lstrip("✔  ").lstrip())
        else:
            self.setStyleSheet(
                "QCheckBox { color: #1e293b; font-size: 10pt; spacing: 10px; }"
                "QCheckBox::indicator { width: 20px; height: 20px; background: #ffffff;"
                "  border: 2px solid #94a3b8; border-radius: 4px; }"
                "QCheckBox::indicator:hover { border-color: #2563eb; background: #eff6ff; }"
            )
            t = self.text()
            if t.startswith("✔  "):
                self.setText(t[3:])

# ─────────────────────────────────────────────────────────────────────────────
# RILEVAMENTO HARDWARE UNIVERSALE
# ─────────────────────────────────────────────────────────────────────────────
def rileva_hardware():
    info = {
        "cpu_threads": os.cpu_count() or 4,
        "cpu_default": max(1, (os.cpu_count() or 4) - 2),
        "encoders":    ["libx265", "libx264"],
        "gpu_parts":   [],
        "gpu_info":    "Nessuna GPU hardware rilevata",
    }
    try:
        out = subprocess.check_output(
            ["ffmpeg", "-hide_banner", "-encoders"],
            text=True, stderr=subprocess.DEVNULL, timeout=10)
        if "hevc_vaapi" in out: info["encoders"].append("hevc_vaapi"); info["gpu_parts"].append("AMD/Intel VAAPI")
        if "hevc_nvenc" in out: info["encoders"].append("hevc_nvenc"); info["gpu_parts"].append("NVIDIA NVENC")
        if "hevc_qsv"   in out: info["encoders"].append("hevc_qsv");   info["gpu_parts"].append("Intel QuickSync")
    except Exception:
        pass
    if info["gpu_parts"]:
        info["gpu_info"] = "GPU: " + ", ".join(info["gpu_parts"])
    return info

HW = rileva_hardware()

# ─────────────────────────────────────────────────────────────────────────────
# SEGNALI
# ─────────────────────────────────────────────────────────────────────────────
class Signals(QObject):
    log        = pyqtSignal(str)
    progresso  = pyqtSignal(str)
    fine       = pyqtSignal(bool)

# ─────────────────────────────────────────────────────────────────────────────
# DIALOGO MANUALE
# ─────────────────────────────────────────────────────────────────────────────
class ManualDialog(QDialog):
    def __init__(self, parent=None, lang="Italiano"):
        super().__init__(parent)
        # Seleziona il manuale nella lingua corrente
        self._manual = MANUALS.get(lang, MANUAL_IT)
        close_label = {"Italiano":"Chiudi","English":"Close","Français":"Fermer",
                       "Deutsch":"Schließen","Español":"Cerrar"}.get(lang,"Close")
        title = {"Italiano":"Manuale","English":"Manual","Français":"Manuel",
                 "Deutsch":"Handbuch","Español":"Manual"}.get(lang,"Manual")
        self.setWindowTitle(f"TitanEncode — {title}")
        self.setMinimumSize(900, 650)
        self.setStyleSheet(STYLE)
        lay = QHBoxLayout(self)
        self.list = QListWidget()
        self.list.setFixedWidth(200)
        self.list.setStyleSheet(
            "QListWidget { background:#f8fafc; border:1px solid #cbd5e1; border-radius:4px; }"
            "QListWidget::item { padding:10px 14px; color:#374151; }"
            "QListWidget::item:selected { background:#dbeafe; color:#1d4ed8; font-weight:bold; }")
        self.stack = QTextBrowser()
        self.stack.setOpenExternalLinks(True)
        self.stack.setStyleSheet(
            "QTextBrowser { background:#ffffff; color:#1e293b; border:1px solid #cbd5e1; "
            "border-radius:4px; padding:16px; font-size:10pt; }")
        for k in self._manual:
            self.list.addItem(k)
        self.list.currentRowChanged.connect(self._show)
        self.list.setCurrentRow(0)
        btn = QPushButton(close_label)
        btn.setStyleSheet(btn_style("#e2e8f0","#1e3a8a","#dbeafe","#1d4ed8"))
        btn.clicked.connect(self.close)
        right = QVBoxLayout()
        right.addWidget(self.stack)
        right.addWidget(btn)
        lay.addWidget(self.list)
        lay.addLayout(right)

    def _show(self, idx):
        key = list(self._manual.keys())[idx]
        self.stack.setHtml(
            "<style>"
            "body{color:#1e293b;background:#ffffff;font-size:10pt;}"
            "h2{color:#1e3a8a;} h3{color:#1d4ed8;}"
            "code,pre{color:#1d4ed8;background:#eff6ff;padding:2px 6px;border-radius:3px;}"
            "table{border-collapse:collapse;width:100%;}"
            "th{background:#1e3a8a;color:#ffffff;padding:6px;}"
            "td{padding:5px 8px;border:1px solid #cbd5e1;}"
            "</style>"
            + self._manual[key])

# ─────────────────────────────────────────────────────────────────────────────
# FINESTRA PRINCIPALE
# ─────────────────────────────────────────────────────────────────────────────
class TitanEncode(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_in      = ""
        self.output_dir   = ""
        self.in_corso     = False
        self._durata_sec  = 0.0
        self._frame_totali = 0  # frame totali rilevati da ffprobe
        self._proc        = None
        self._lang        = "Italiano"
        self.signals      = Signals()
        self.signals.log.connect(self.update_console)
        self.signals.fine.connect(self.on_fine)
        self.signals.progresso.connect(self.update_progresso)
        self.setMinimumSize(1320, 1000)
        self.setStyleSheet(STYLE)
        # Icona applicazione — cerca TitanEncode.png nella stessa cartella dello script
        _icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TitanEncode.png")
        if os.path.exists(_icon_path):
            self.setWindowIcon(QIcon(_icon_path))
        self._build_ui()
        self._apply_lang()
        self.lbl_sub.setToolTip(
            f"CPU: {HW['cpu_threads']} thread  —  default encoding: {HW['cpu_default']} thread\n"
            f"{HW['gpu_info']}")

    def T(self, key):
        return LANGS[self._lang].get(key, key)

    # ── BUILD UI ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Menu bar
        mb = self.menuBar()
        self.m_file = mb.addMenu("File")
        self.act_load  = QAction("Load", self); self.act_load.triggered.connect(self.carica_film)
        self.act_reset = QAction("Reset", self); self.act_reset.triggered.connect(self.reset_tutto)
        self.act_exit  = QAction("Exit", self);  self.act_exit.triggered.connect(self.close)
        self.m_file.addAction(self.act_load)
        self.m_file.addAction(self.act_reset)
        self.m_file.addSeparator()
        self.m_file.addAction(self.act_exit)

        self.m_options = mb.addMenu("Options")
        self.m_lang = QMenu("Language", self)
        self.lang_actions = {}
        for lng in LANGS:
            a = QAction(lng, self)
            a.triggered.connect(lambda checked, l=lng: self._set_lang(l))
            self.m_lang.addAction(a)
            self.lang_actions[lng] = a
        self.m_options.addMenu(self.m_lang)

        self.m_help = mb.addMenu("Help")
        self.act_manual = QAction("Manual", self); self.act_manual.triggered.connect(self._show_manual)
        self.act_about  = QAction("About",  self); self.act_about.triggered.connect(self._show_about)
        self.m_help.addAction(self.act_manual)
        self.m_help.addAction(self.act_about)

        # Central
        cw = QWidget(); self.setCentralWidget(cw)
        ml = QVBoxLayout(cw); ml.setContentsMargins(16,10,16,12); ml.setSpacing(8)

        # Header
        hf = QFrame()
        hf.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
                         "stop:0 #1e3a8a,stop:0.5 #1d4ed8,stop:1 #1e3a8a);"
                         "border: 2px solid #2563eb; border-radius: 14px;")
        hl = QVBoxLayout(hf); hl.setContentsMargins(20,10,20,10)
        self.lbl_title = QLabel("TitanEncode")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setStyleSheet(
            "font-size: 38pt; font-weight: 900; color: #ffffff; border: none; letter-spacing: 6px;")
        self.lbl_sub = QLabel("")
        self.lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_sub.setStyleSheet("font-size: 8pt; color: #93c5fd; border: none;")
        hl.addWidget(self.lbl_title); hl.addWidget(self.lbl_sub)
        ml.addWidget(hf)

        # Tabs
        self.tabs = QTabWidget()
        ml.addWidget(self.tabs)
        self._build_tab_video()
        self._build_tab_filtri()
        self._build_tab_avanzato()
        self._build_tab_audio()

        # Log
        self.lbl_report = QLabel("")
        self.lbl_report.setStyleSheet("color:#1e3a8a; font-weight:bold; font-size:10pt;")
        self.console = QTextEdit(); self.console.setReadOnly(True)
        self.console.setMaximumHeight(180)
        ml.addWidget(self.lbl_report); ml.addWidget(self.console)

        # Output dir row
        out_row = QHBoxLayout(); out_row.setSpacing(8)
        self.lbl_out_label = QLabel("")
        self.lbl_out_label.setStyleSheet("color:#1e3a8a; font-weight:bold; font-size:10pt;")
        self.lbl_out_label.setFixedWidth(90)
        self.lbl_out_path = QLabel("")
        self.lbl_out_path.setStyleSheet(
            "background:#f8fafc; color:#64748b; border:1px solid #cbd5e1; "
            "border-radius:4px; padding:4px 10px; font-size:9pt;")
        self.btn_out_choose = QPushButton("")
        self.btn_out_choose.setFixedHeight(32)
        self.btn_out_choose.setStyleSheet(btn_style("#1a2a4a","#4a9eff","#2a3a6a",9))
        self.btn_out_choose.clicked.connect(self.scegli_output)
        self.btn_out_reset = QPushButton("✕")
        self.btn_out_reset.setFixedSize(32,32)
        self.btn_out_reset.setToolTip("Ripristina cartella sorgente")
        self.btn_out_reset.setStyleSheet(btn_style("#2a1a1a","#ff6666","#4a2a2a",10))
        self.btn_out_reset.clicked.connect(self.reset_output_dir)
        out_row.addWidget(self.lbl_out_label)
        out_row.addWidget(self.lbl_out_path, 1)
        out_row.addWidget(self.btn_out_choose)
        out_row.addWidget(self.btn_out_reset)
        ml.addLayout(out_row)

        # Progress
        self.lbl_progress = QLabel("")
        self.lbl_progress.setStyleSheet("color:#1e3a8a; font-weight:bold; font-size:10pt;")
        self.bar = QProgressBar()
        self.bar.setRange(0,1000); self.bar.setValue(0)
        self.bar.setFixedHeight(26); self.bar.setFormat("  %p%")
        ml.addWidget(self.lbl_progress); ml.addWidget(self.bar)

        # Footer buttons
        foot = QHBoxLayout(); foot.setSpacing(10)
        self.btn_load  = QPushButton("")
        self.btn_load.setFixedHeight(54)
        self.btn_load.setStyleSheet(btn_style("#16a34a","#ffffff","#15803d"))
        self.btn_load.clicked.connect(self.carica_film)

        self.btn_reset = QPushButton("")
        self.btn_reset.setFixedHeight(54)
        self.btn_reset.setStyleSheet(btn_style("#e2e8f0","#475569","#cbd5e1","#1e293b"))
        self.btn_reset.clicked.connect(self.reset_tutto)

        self.btn_stop  = QPushButton("")
        self.btn_stop.setFixedHeight(54); self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet(btn_style("#fee2e2","#dc2626","#fecaca","#991b1b"))
        self.btn_stop.clicked.connect(self.stop_encoding)

        self.btn_go    = QPushButton("")
        self.btn_go.setFixedHeight(72); self.btn_go.setEnabled(False)
        self.btn_go.setStyleSheet(btn_style("#dc2626","#ffffff","#b91c1c","#ffffff",15))
        self.btn_go.clicked.connect(self.avvia_encoding)

        foot.addWidget(self.btn_load)
        foot.addWidget(self.btn_reset)
        foot.addStretch()
        foot.addWidget(self.btn_stop)
        foot.addWidget(self.btn_go)
        ml.addLayout(foot)

    # ── TABS ─────────────────────────────────────────────────────────────────
    def _build_tab_video(self):
        t = QWidget(); lay = QVBoxLayout(t)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        cont = QWidget(); self.fx_video = QFormLayout(cont)
        self.fx_video.setSpacing(14); self.fx_video.setContentsMargins(24,20,24,20)

        # Encoder — rilevato automaticamente all'avvio (vedi HW globale)
        self.v_enc = QComboBox()
        self.v_enc.addItems(HW["encoders"])

        self.v_rf      = QDoubleSpinBox(); self.v_rf.setRange(0,51); self.v_rf.setValue(20.0); self.v_rf.setSingleStep(0.5)
        self.v_fps     = QComboBox(); self.v_fps.addItems(["Originale (Source)","23.976","24","25","50","60"])
        self.v_pre     = QComboBox()
        self.v_pre.addItems(["ultrafast","superfast","veryfast","faster","fast","medium","slow","slower","veryslow"])
        self.v_pre.setCurrentText("slow")
        self.v_range   = QComboBox(); self.v_range.addItems(["Originale","tv (Limited 16-235)","pc (Full 0-255)"])
        self.v_bit     = QComboBox(); self.v_bit.addItems(["10-bit (HDR)","8-bit"])
        self.v_maxrate = QSpinBox(); self.v_maxrate.setRange(0,200000); self.v_maxrate.setValue(0); self.v_maxrate.setSuffix(" kbps")
        self.v_bufsize = QSpinBox(); self.v_bufsize.setRange(0,400000); self.v_bufsize.setValue(0); self.v_bufsize.setSuffix(" kbps")
        self.ck_web    = SpuntaCheck(); self.ck_web.setChecked(True)
        self.ck_hdr    = SpuntaCheck(); self.ck_hdr.setChecked(True)
        self.ck_hdrcopy= SpuntaCheck(); self.ck_hdrcopy.setChecked(False)

        # Tooltips video
        self.v_enc.setToolTip(
            "libx265    \u2192 qualit\u00e0 massima HDR/4K (consigliato)\n"
            "libx264    \u2192 compatibilit\u00e0 universale, pi\u00f9 veloce\n"
            "hevc_vaapi \u2192 GPU AMD/Intel, veloce, qualit\u00e0 minore\n"
            "hevc_nvenc \u2192 GPU NVIDIA, veloce, qualit\u00e0 minore\n"
            f"\n{HW['gpu_info']}")
        self.v_rf.setToolTip("Qualità: valori più bassi = file più grande, qualità migliore\n18-20 → qualità quasi-lossless\n22-24 → buona qualità, file compatto")
        self.v_pre.setToolTip("Velocità encoding: preset più lento = file più piccolo a parità RF\nslow → ottimo compromesso qualità/tempo\nveryslow → archivio definitivo")
        self.ck_web.setToolTip("Sposta il moov atom all'inizio — necessario per streaming\nAggiunge anche sync A/V (avoid_negative_ts)")
        self.ck_hdr.setToolTip("Inserisce metadati HDR10 (master-display, max-cll)\nNecessario per la corretta resa sui TV HDR")

        from PyQt6.QtWidgets import QLabel as _QL
        self._v_rows = [
            ("enc_video", self.v_enc), ("enc_quality", self.v_rf),
            ("enc_fps", self.v_fps),   ("enc_preset", self.v_pre),
            ("enc_range", self.v_range), ("enc_depth", self.v_bit),
            ("enc_maxrate", self.v_maxrate), ("enc_bufsize", self.v_bufsize),
        ]
        self._v_labels = []
        for key, w in self._v_rows:
            lbl = _QL("")
            lbl.setStyleSheet("color:#374151; font-size:10pt; font-weight:500;")
            self._v_labels.append(lbl)
            self.fx_video.addRow(lbl, w)
        self.fx_video.addRow(self.ck_web)
        self.fx_video.addRow(self.ck_hdr)
        self.fx_video.addRow(self.ck_hdrcopy)

        scroll.setWidget(cont); lay.addWidget(scroll)
        self.tabs.addTab(t, "VIDEO")

    def _build_tab_filtri(self):
        t = QWidget(); lay = QVBoxLayout(t)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        cont = QWidget(); self.fx_filt = QFormLayout(cont)
        self.fx_filt.setSpacing(14); self.fx_filt.setContentsMargins(24,20,24,20)

        self.f_aq    = QComboBox(); self.f_aq.addItems(["1: Standard","2: Auto-Varianza","3: Dark Scene"])
        self.f_psy   = QDoubleSpinBox(); self.f_psy.setRange(0,5); self.f_psy.setValue(2.0); self.f_psy.setSingleStep(0.1)
        self.f_psycb = QDoubleSpinBox(); self.f_psycb.setRange(0,5); self.f_psycb.setValue(0.1); self.f_psycb.setSingleStep(0.05)
        self.f_sh    = QDoubleSpinBox(); self.f_sh.setRange(0,5); self.f_sh.setValue(1.0); self.f_sh.setSingleStep(0.1)
        self.f_dn    = QDoubleSpinBox(); self.f_dn.setRange(0,5); self.f_dn.setValue(0.0); self.f_dn.setSingleStep(0.1)
        self.f_gamma = QDoubleSpinBox(); self.f_gamma.setRange(0.1,3.0); self.f_gamma.setValue(1.0); self.f_gamma.setSingleStep(0.05)
        self.f_sat   = QDoubleSpinBox(); self.f_sat.setRange(0.0,3.0); self.f_sat.setValue(1.0); self.f_sat.setSingleStep(0.05)
        self.f_deband= SpuntaCheck(); self.f_deband.setChecked(True)
        self.f_deband_str = QDoubleSpinBox(); self.f_deband_str.setRange(0.1,4.0); self.f_deband_str.setValue(1.2); self.f_deband_str.setSingleStep(0.1)
        self.f_crop  = SpuntaCheck(); self.f_crop.setChecked(True)
        self.f_nlm   = SpuntaCheck(); self.f_nlm.setChecked(False)
        self.f_yadif = SpuntaCheck(); self.f_yadif.setChecked(False)
        self.f_scale = QComboBox(); self.f_scale.addItems(["Originale","3840x2160 (4K)","1920x1080 (FHD)","1280x720 (HD)"])
        self.f_scale_algo = QComboBox(); self.f_scale_algo.addItems(["lanczos","bicubic","bilinear","spline"])

        # ── Tooltip TAB FILTRI ────────────────────────────────────────────
        self.f_aq.setToolTip(
            "Come x265 distribuisce i bit.\n"
            "1 Standard      \u2192 uniforme\n"
            "2 Auto-Varianza \u2192 analizza ogni frame (consigliato)\n"
            "3 Dark Scene    \u2192 ottimizzato scene buie HDR")
        self.f_psy.setToolTip(
            "Psy-RD Luma: preserva il dettaglio visivo sulla luminanza.\n"
            "1.5\u20132.5 \u2192 ottimale per film HDR\n"
            "Sopra 3.0 \u2192 artefatti su superfici lisce")
        self.f_psycb.setToolTip(
            "Psy-RDO Chroma: preserva saturazione e dettaglio colore.\n"
            "0.0\u20130.2 \u2192 sicuro per HDR BT.2020\n"
            "Valori alti \u2192 rumore colorato nelle ombre")
        self.f_sh.setToolTip(
            "Nitidezza unsharp mask.\n"
            "0.0      \u2192 disattivo\n"
            "0.5\u20131.5 \u2192 leggera, buona per Blu-ray\n"
            "2.0+     \u2192 aggressiva, per upscaling\n"
            "\u26a0\ufe0f Non usare con NL-Means attivo")
        self.f_dn.setToolTip(
            "Riduzione rumore hqdn3d.\n"
            "0.0      \u2192 disattivo (consigliato per 4K)\n"
            "0.5\u20131.5 \u2192 leggero, utile per DVD/TV\n"
            "\u26a0\ufe0f Rimuove anche il dettaglio fine")
        self.f_gamma.setToolTip(
            "Correzione gamma.\n"
            "1.00    \u2192 originale (corretto per HDR)\n"
            "< 1.00  \u2192 schiarisce ombre\n"
            "> 1.00  \u2192 scurisce mezze luci\n"
            "\u26a0\ufe0f Su HDR/PQ non modificare: rompe la calibrazione")
        self.f_sat.setToolTip(
            "Saturazione colore.\n"
            "1.00   \u2192 originale (consigliato HDR BT.2020)\n"
            "< 1.00 \u2192 desatura\n"
            "> 1.00 \u2192 ipersatura")
        self.f_deband.setToolTip(
            "Rimuove il banding (gradienti a scalini).\n"
            "Filtro deband nativo FFmpeg, ottimizzato per 10-bit HDR.\n"
            "\u2705 Tienilo attivo: il banding \u00e8 comune anche nei Blu-ray 4K.")
        self.f_deband_str.setToolTip(
            "Intensit\u00e0 del deband.\n"
            "0.5\u20131.0 \u2192 leggero, preserva dettaglio\n"
            "1.2     \u2192 default bilanciato HDR\n"
            "2.0+    \u2192 aggressivo, pu\u00f2 ammorbidire gradienti fini")
        self.f_crop.setToolTip(
            "Rileva e rimuove bande nere (letterbox/pillarbox).\n"
            "Analizza 500 frame per trovare il crop sicuro.\n"
            "\u2705 Attivalo sempre: i bordi neri sprecano bit.")
        self.f_nlm.setToolTip(
            "NL-Means: denoise qualit\u00e0 superiore a hqdn3d.\n"
            "Pro: preserva meglio bordi e texture\n"
            "Contro: molto pi\u00f9 lento\n"
            "Usalo solo per sorgenti rumorose: DVD, VHS, analogiche.")
        self.f_yadif.setToolTip(
            "De-interlace YADIF.\n"
            "\u26a0\ufe0f Attiva SOLO per sorgenti interlacciate (TV, DVD PAL).\n"
            "Blu-ray e file digitali sono gi\u00e0 progressivi \u2014 non usare.")
        self.f_scale.setToolTip(
            "Ridimensiona la risoluzione.\n"
            "Originale \u2192 nessun ridimensionamento (consigliato)\n"
            "4K        \u2192 upscaling a 3840x2160\n"
            "FHD       \u2192 downscaling a 1920x1080")
        self.f_scale_algo.setToolTip(
            "Algoritmo di interpolazione.\n"
            "lanczos  \u2192 migliore qualit\u00e0 (consigliato)\n"
            "bicubic  \u2192 buona qualit\u00e0, pi\u00f9 morbido\n"
            "bilinear \u2192 veloce, perde nitidezza")

        self._f_rows = [
            ("flt_aq",self.f_aq), ("flt_psy",self.f_psy), ("flt_psycb",self.f_psycb),
            ("flt_sharp",self.f_sh), ("flt_denoise",self.f_dn), ("flt_gamma",self.f_gamma),
            ("flt_sat",self.f_sat), ("flt_deband_str",self.f_deband_str),
            ("flt_scale",self.f_scale), ("flt_scale_algo",self.f_scale_algo),
        ]
        self.fx_filt.addRow(self.f_deband)
        self._f_labels = []
        for key, w in self._f_rows:
            lbl = QLabel("")
            lbl.setStyleSheet("color:#374151; font-size:10pt; font-weight:500;")
            self._f_labels.append(lbl)
            self.fx_filt.addRow(lbl, w)
        self.fx_filt.addRow(self.f_crop)
        self.fx_filt.addRow(self.f_nlm)
        self.fx_filt.addRow(self.f_yadif)

        scroll.setWidget(cont); lay.addWidget(scroll)
        self.tabs.addTab(t, "FILTRI")

    def _build_tab_avanzato(self):
        t = QWidget(); lay = QVBoxLayout(t)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        cont = QWidget(); self.fx_adv = QFormLayout(cont)
        self.fx_adv.setSpacing(14); self.fx_adv.setContentsMargins(24,20,24,20)

        self.x_bframes  = QSpinBox(); self.x_bframes.setRange(0,16); self.x_bframes.setValue(8)
        self.x_badapt   = QComboBox(); self.x_badapt.addItems(["0: Off","1: Fast","2: Full"]); self.x_badapt.setCurrentText("2: Full")
        self.x_lookahead= QSpinBox(); self.x_lookahead.setRange(0,250); self.x_lookahead.setValue(60)
        self.x_deblock  = QLineEdit("-1,-1")
        self.x_merange  = QSpinBox(); self.x_merange.setRange(0,256); self.x_merange.setValue(57)
        self.x_subme    = QSpinBox(); self.x_subme.setRange(0,11); self.x_subme.setValue(7)
        self.x_me       = QComboBox(); self.x_me.addItems(["dia","hex","umh","star","sea","full"]); self.x_me.setCurrentText("umh")
        self.x_ref      = QSpinBox(); self.x_ref.setRange(1,16); self.x_ref.setValue(4)
        self.x_open_gop = QCheckBox("Open GOP"); self.x_open_gop.setChecked(False)
        self.x_scenecut = QSpinBox(); self.x_scenecut.setRange(0,100); self.x_scenecut.setValue(40)
        self.x_keyint   = QSpinBox(); self.x_keyint.setRange(0,1000); self.x_keyint.setValue(250)
        self.x_threads  = QSpinBox(); self.x_threads.setRange(0,64); self.x_threads.setValue(HW['cpu_default'])
        self.x_hdr_mdcv = QLineEdit("G(13250,34500)B(7500,3000)R(34000,16000)WP(15635,16450)L(10000000,1)")
        self.x_hdr_cll  = QLineEdit("1000,400")

        # ── Tooltip TAB AVANZATO ───────────────────────────────────────
        self.x_bframes.setToolTip(
            "B-frame tra due frame di riferimento.\n"
            "8 \u2192 ottimale per film\n"
            "0 \u2192 disabilita (non consigliato)")
        self.x_badapt.setToolTip(
            "Come x265 decide quanti B-frame usare.\n"
            "2 Full \u2192 analisi completa, migliore (consigliato)\n"
            "1 Fast \u2192 pi\u00f9 veloce ma meno preciso")
        self.x_lookahead.setToolTip(
            "Frame analizzati in anticipo per decisioni bitrate.\n"
            "60 \u2192 ottimale per film (~2-3 sec a 24fps)\n"
            "\u26a0\ufe0f Valori alti aumentano l'uso di RAM")
        self.x_deblock.setToolTip(
            "Filtro deblock in-loop (forza,soglia).\n"
            "-1,-1 \u2192 leggermente morbido, ottimo per film\n"
            " 0, 0 \u2192 default x265\n"
            "-2,-2 \u2192 minimo deblock, massimo dettaglio")
        self.x_merange.setToolTip(
            "Raggio ricerca movimento (pixel).\n"
            "57 \u2192 ottimale per 4K con preset slow+\n"
            "\u26a0\ufe0f Valori alti rallentano molto l'encoding")
        self.x_subme.setToolTip(
            "Precisione stima sub-pixel del movimento.\n"
            "7 \u2192 analisi completa con distorsione RD (consigliato)\n"
            "\u26a0\ufe0f subme=7 \u00e8 molto pi\u00f9 lento di subme=4")
        self.x_me.setToolTip(
            "Algoritmo Motion Estimation.\n"
            "umh  \u2192 ottimale per film (consigliato)\n"
            "hex  \u2192 buon compromesso velocit\u00e0/qualit\u00e0\n"
            "full \u2192 esaustivo, troppo lento per uso normale")
        self.x_ref.setToolTip(
            "Frame di riferimento per ogni frame.\n"
            "4 \u2192 ottimale con preset slow+\n"
            "\u26a0\ufe0f Oltre 8 non porta benefici visivi")
        self.x_open_gop.setToolTip(
            "Permette riferimenti al GOP precedente.\n"
            "Pro: compressione leggermente migliore\n"
            "\u26a0\ufe0f Pu\u00f2 causare problemi di seeking \u2014 tienilo disattivo")
        self.x_scenecut.setToolTip(
            "Sensibilit\u00e0 rilevamento cambi scena (0\u2013100).\n"
            "40 \u2192 default bilanciato\n"
            "0  \u2192 disattiva (non consigliato)")
        self.x_keyint.setToolTip(
            "Distanza massima tra keyframe.\n"
            "250 \u2192 ~10 sec a 24fps, buono per film\n"
            "Per streaming: 48-72 (2-3 sec a 24fps)")
        self.x_threads.setToolTip(
            f"Thread CPU per x265.\n"
            f"CPU rilevata: {HW['cpu_threads']} thread logici\n"
            f"Default consigliato: {HW['cpu_default']} thread\n"
            f"{HW['gpu_info']}\n"
            "0 \u2192 automatico (usa tutti i thread)\n"
            "\u26a0\ufe0f Con tutti i thread il desktop pu\u00f2 congelare")
        self.x_hdr_mdcv.setToolTip(
            "Mastering Display Color Volume (SMPTE ST 2086).\n"
            "\u2705 Letto automaticamente dalla sorgente al caricamento.\n"
            "Formato: G(x,y)B(x,y)R(x,y)WP(x,y)L(max*10000,min*10000)")
        self.x_hdr_cll.setToolTip(
            "Content Light Level (CEA 861.3).\n"
            "MaxCLL  \u2192 picco luminosit\u00e0 pixel pi\u00f9 brillante (nit)\n"
            "MaxFALL \u2192 media frame pi\u00f9 luminoso (nit)\n"
            "\u2705 Letto automaticamente al caricamento.\n"
            "\u26a0\ufe0f Il TV usa questi valori per il tone mapping HDR.")

        self._adv_rows = [
            ("adv_bframes",self.x_bframes), ("adv_badapt",self.x_badapt),
            ("adv_lookahead",self.x_lookahead), ("adv_deblock",self.x_deblock),
            ("adv_merange",self.x_merange), ("adv_subme",self.x_subme),
            ("adv_me",self.x_me), ("adv_ref",self.x_ref),
            ("adv_scenecut",self.x_scenecut), ("adv_keyint",self.x_keyint),
            ("adv_threads",self.x_threads), ("adv_mdcv",self.x_hdr_mdcv),
            ("adv_cll",self.x_hdr_cll),
        ]
        self.fx_adv.addRow(self.x_open_gop)
        self._adv_labels = []
        for key, w in self._adv_rows:
            lbl = QLabel("")
            lbl.setStyleSheet("color:#374151; font-size:10pt; font-weight:500;")
            self._adv_labels.append(lbl)
            self.fx_adv.addRow(lbl, w)

        scroll.setWidget(cont); lay.addWidget(scroll)
        self.tabs.addTab(t, "AVANZATO")

    def _build_tab_audio(self):
        t = QWidget(); lay = QVBoxLayout(t)
        # Tabella solo AUDIO e SUB — VIDEO esclusi al caricamento
        # Colonne: ID | Lingua | Codec | Ch | Titolo | Azione | DEF | FOR
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(["ID","Lingua","Codec","Ch","Titolo","Azione","DEF","FOR"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        lay.addWidget(self.table)
        self.tabs.addTab(t, "AUDIO")

    # ── LINGUA ───────────────────────────────────────────────────────────────
    def _set_lang(self, lang):
        self._lang = lang
        self._apply_lang()

    def _apply_lang(self):
        T = self.T
        self.setWindowTitle(T("app_title"))
        self.lbl_sub.setText(T("header_sub"))
        self.lbl_report.setText(T("lbl_report"))
        self.lbl_out_label.setText(T("lbl_output"))
        self.lbl_out_path.setText(T("lbl_out_default") if not self.output_dir else self.output_dir)
        self.lbl_progress.setText(T("lbl_ready"))
        self.btn_load.setText(T("btn_load"))
        self.btn_reset.setText(T("btn_reset"))
        self.btn_go.setText(T("btn_start"))
        self.btn_stop.setText(T("btn_stop"))
        self.btn_out_choose.setText(T("btn_choose_out"))
        # Menu
        self.m_file.setTitle(T("menu_file"))
        self.m_options.setTitle(T("menu_options"))
        self.m_help.setTitle(T("menu_help"))
        self.m_lang.setTitle(T("menu_lang"))
        self.act_load.setText(T("menu_load"))
        self.act_reset.setText(T("menu_reset"))
        self.act_exit.setText(T("menu_exit"))
        self.act_manual.setText(T("menu_manual"))
        self.act_about.setText(T("menu_about"))
        # Tab names
        self.tabs.setTabText(0, T("tab_video"))
        self.tabs.setTabText(1, T("tab_filters"))
        self.tabs.setTabText(2, T("tab_advanced"))
        self.tabs.setTabText(3, T("tab_audio"))
        # Form labels video — aggiorna direttamente i QLabel salvati
        for lbl, (key, _) in zip(self._v_labels, self._v_rows):
            lbl.setText(T(key))
        self.ck_web.setText(T("enc_web"))
        self.ck_hdr.setText(T("enc_hdr"))
        self.ck_hdrcopy.setText(T("enc_hdrcopy"))
        # Form labels filtri
        for lbl, (key, _) in zip(self._f_labels, self._f_rows):
            lbl.setText(T(key))
        self.f_deband.setText(T("flt_deband"))
        self.f_crop.setText(T("flt_crop"))
        self.f_nlm.setText(T("flt_nlm"))
        self.f_yadif.setText(T("flt_yadif"))
        # Form labels avanzato
        for lbl, (key, _) in zip(self._adv_labels, self._adv_rows):
            lbl.setText(T(key))
        self.x_open_gop.setText(T("adv_opengop"))
        # Audio table headers
        self.table.setHorizontalHeaderLabels([
            T("aud_col_id"), T("aud_col_lang"), T("aud_col_codec"),
            T("aud_col_ch"), T("aud_col_title"), T("aud_col_action"),
            T("aud_col_def"), T("aud_col_forced")
        ])

    # ── CARICA FILM ──────────────────────────────────────────────────────────
    def carica_film(self):
        f, _ = QFileDialog.getOpenFileName(self, self.T("menu_load"), "",
            "Video (*.mkv *.mp4 *.ts *.avi *.mov *.m2ts *.wmv);;All (*)")
        if not f: return
        self.file_in = f
        self.console.clear()
        self.lbl_report.setText(f"{self.T('lbl_report')}  {os.path.basename(f)}")
        try:
            res = subprocess.check_output(
                ["ffprobe","-v","quiet","-print_format","json","-show_streams", f],
                text=True, stderr=subprocess.DEVNULL)
            streams = json.loads(res).get("streams",[])
            self.table.setRowCount(0)
            vid_c = aud_c = sub_c = 0

            for s in streams:
                ct = s.get("codec_type","").upper()
                if ct == "VIDEO":
                    vid_c += 1; continue        # VIDEO non appare nella tabella audio
                if ct not in ("AUDIO","SUBTITLE"): continue
                tipo = "SUBTITLES" if ct == "SUBTITLE" else "AUDIO"
                if ct == "AUDIO": aud_c += 1
                else: sub_c += 1

                r = self.table.rowCount(); self.table.insertRow(r)
                tags = s.get("tags",{})
                stream_idx = s.get("index", r)

                self.table.setItem(r,0,QTableWidgetItem(str(stream_idx)))
                self.table.setItem(r,1,QTableWidgetItem(tags.get("language", tags.get("LANGUAGE","und"))))
                self.table.setItem(r,2,QTableWidgetItem(s.get("codec_name","-").upper()))
                self.table.setItem(r,3,QTableWidgetItem(str(s.get("channels",""))))
                self.table.setItem(r,4,QTableWidgetItem(tags.get("title", tags.get("TITLE","-"))))

                # Colonna azione — semplificata: Mantieni / Converti / Rimuovi
                # Per subtitles: solo Mantieni / Rimuovi
                cb = QComboBox()
                if tipo == "AUDIO":
                    cb.addItems([
                        self.T("aud_keep"),
                        f"{self.T('aud_convert')} E-AC3 640k",
                        f"{self.T('aud_convert')} E-AC3 1536k",
                        f"{self.T('aud_convert')} AAC 256k",
                        f"{self.T('aud_convert')} AAC 192k",
                        self.T("aud_remove"),
                    ])
                else:
                    cb.addItems([self.T("aud_keep"), self.T("aud_remove")])
                self.table.setCellWidget(r,5,cb)

                # Colonna tipo interno (nascosta — usata dal motore)
                self.table.item(r,0).setData(Qt.ItemDataRole.UserRole, tipo)

                # Leggi i flag default e forced GIÀ presenti nel file sorgente
                # FFprobe li riporta come "disposition" — li specchiamo esattamente
                disp        = s.get("disposition", {})
                is_default  = bool(disp.get("default",  0))
                is_forced   = bool(disp.get("forced",   0))

                for col in [6, 7]:
                    ck = SpuntaCheck()
                    # Pre-spunta basata sui flag originali della sorgente
                    ck.setChecked(is_default if col == 6 else is_forced)
                    if col == 6:
                        stato = "✅ già DEFAULT nel sorgente" if is_default else "non è default nel sorgente"
                        ck.setToolTip(
                            f"▶ AUTO-PLAY — parte automaticamente senza selezione manuale.\n"
                            f"Stato nel file originale: {stato}\n"
                            f"Attiva su una sola traccia audio e una sola sub per lingua.")
                    else:
                        stato = "✅ già FORCED nel sorgente" if is_forced else "non è forced nel sorgente"
                        ck.setToolTip(
                            f"🔒 FORZATO — appare sempre anche con i sub disattivati.\n"
                            f"Usato per dialoghi in lingua straniera dentro il film.\n"
                            f"Stato nel file originale: {stato}")
                    self.table.setCellWidget(r, col, ck)

            self.btn_go.setEnabled(True)

            # Durata e frame totali
            res2 = subprocess.check_output(
                ["ffprobe","-v","quiet","-print_format","json","-show_format",f],
                text=True, stderr=subprocess.DEVNULL)
            fmt = json.loads(res2).get("format",{})
            try:
                self._durata_sec = float(fmt.get("duration",0))
                hh=int(self._durata_sec//3600); mm=int((self._durata_sec%3600)//60); ss=int(self._durata_sec%60)
                dur_str = f"{hh:02d}:{mm:02d}:{ss:02d}"
            except Exception:
                self._durata_sec = 0.0; dur_str = "?"

            # Leggi frame totali da ffprobe per barra progresso affidabile
            try:
                res3 = subprocess.check_output(
                    ["ffprobe","-v","quiet","-print_format","json",
                     "-show_streams","-select_streams","v:0",f],
                    text=True, stderr=subprocess.DEVNULL)
                vs = json.loads(res3).get("streams",[{}])[0]
                # Prova nb_frames prima, poi calcola da duration e fps
                nb = vs.get("nb_frames","")
                if nb and nb.isdigit():
                    self._frame_totali = int(nb)
                else:
                    # Calcola da durata × fps
                    fps_str = vs.get("r_frame_rate","24/1")
                    num, den = fps_str.split("/")
                    fps = float(num)/float(den)
                    self._frame_totali = int(self._durata_sec * fps)
                if self._frame_totali > 0:
                    self.update_console(f"   Frame totali: {self._frame_totali:,}")
            except Exception:
                self._frame_totali = 0

            self.update_console(f"{self.T('file_loaded')} {f}")
            self.update_console(self.T("file_tracks").format(vid_c,aud_c,sub_c,dur_str))
            self._leggi_hdr_ffprobe(f)

        except Exception as e:
            self.update_console(f"❌ {e}")

    def _leggi_hdr_ffprobe(self, fp):
        """Legge metadati HDR dalla sorgente.
        Se la sorgente è SDR disabilita automaticamente il checkbox HDR
        per evitare errori FFmpeg (codice 234) durante l'encoding."""
        try:
            res = subprocess.check_output(
                ["ffprobe","-v","quiet","-print_format","json","-show_streams","-select_streams","v:0",fp],
                text=True, stderr=subprocess.DEVNULL)
            s = json.loads(res).get("streams",[{}])[0]

            # Controlla se la sorgente è HDR verificando transfer characteristics
            transfer = s.get("color_transfer","")
            is_hdr = transfer in ("smpte2084","arib-std-b67","smpte428")

            hdr_trovato = False
            for sd in s.get("side_data_list",[]):
                if "Mastering" in sd.get("side_data_type",""):
                    def to_i(v, mul=50000):
                        try:
                            parts = str(v).split("/")
                            return int(round(float(parts[0])/float(parts[1])*mul)) if len(parts)==2 else int(float(v)*mul)
                        except: return 0
                    mdcv = (f"G({to_i(sd.get('green_x'))},{to_i(sd.get('green_y'))})"
                            f"B({to_i(sd.get('blue_x'))},{to_i(sd.get('blue_y'))})"
                            f"R({to_i(sd.get('red_x'))},{to_i(sd.get('red_y'))})"
                            f"WP({to_i(sd.get('white_point_x'))},{to_i(sd.get('white_point_y'))})"
                            f"L({to_i(sd.get('max_luminance'),10000)},{to_i(sd.get('min_luminance'),10000)})")
                    self.x_hdr_mdcv.setText(mdcv)
                    self.update_console(f"{self.T('hdr_found_mdcv')} {mdcv}")
                    hdr_trovato = True
                if "Content" in sd.get("side_data_type","") and "Light" in sd.get("side_data_type",""):
                    cll = f"{sd.get('max_content',0)},{sd.get('max_average',0)}"
                    self.x_hdr_cll.setText(cll)
                    self.update_console(f"{self.T('hdr_found_cll')} {cll}")

            # Attiva/disattiva HDR passthrough in base alla sorgente
            if hdr_trovato or is_hdr:
                self.ck_hdr.setChecked(True)
                self.update_console("   🎨 Sorgente HDR — Passthrough HDR10 attivato")
            else:
                self.ck_hdr.setChecked(False)
                self.x_hdr_mdcv.setText("")
                self.x_hdr_cll.setText("")
                self.update_console("   ℹ️  Sorgente SDR — Passthrough HDR disattivato")

        except Exception: pass

    # ── OUTPUT DIR ───────────────────────────────────────────────────────────
    def scegli_output(self):
        d = QFileDialog.getExistingDirectory(self, "", self.output_dir or os.path.expanduser("~"))
        if d:
            self.output_dir = d
            self.lbl_out_path.setText(d)
            self.lbl_out_path.setStyleSheet(
                "background:#12131f; color:#4a9eff; border:1px solid #4a9eff; "
                "border-radius:4px; padding:4px 10px; font-size:9pt;")
            self.update_console(f"{self.T('out_set')} {d}")

    def reset_output_dir(self):
        self.output_dir = ""
        self.lbl_out_path.setText(self.T("lbl_out_default"))
        self.lbl_out_path.setStyleSheet(
            "background:#f8fafc; color:#64748b; border:1px solid #cbd5e1; "
            "border-radius:4px; padding:4px 10px; font-size:9pt;")

    # ── RESET ────────────────────────────────────────────────────────────────
    def reset_tutto(self):
        if self.in_corso:
            QMessageBox.warning(self,"",self.T("stop_warning")); return
        r = QMessageBox.question(self, self.T("reset_title"), self.T("reset_msg"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if r != QMessageBox.StandardButton.Yes: return
        self.file_in = ""; self.output_dir = ""
        self.table.setRowCount(0)
        self.console.clear()
        self.bar.setValue(0)
        self.btn_go.setEnabled(False)
        self.lbl_report.setText(self.T("lbl_report"))
        self.lbl_progress.setText(self.T("lbl_ready"))
        self.reset_output_dir()
        # Reset valori default
        self.v_enc.setCurrentIndex(0); self.v_rf.setValue(20.0)
        self.v_fps.setCurrentIndex(0); self.v_pre.setCurrentText("slow")
        self.v_range.setCurrentIndex(0); self.v_bit.setCurrentIndex(0)
        self.v_maxrate.setValue(0); self.v_bufsize.setValue(0)
        self.ck_web.setChecked(True); self.ck_hdr.setChecked(True); self.ck_hdrcopy.setChecked(False)
        self.f_aq.setCurrentIndex(0); self.f_psy.setValue(2.0); self.f_psycb.setValue(0.1)
        self.f_sh.setValue(1.0); self.f_dn.setValue(0.0); self.f_gamma.setValue(1.0)
        self.f_sat.setValue(1.0); self.f_deband.setChecked(True); self.f_deband_str.setValue(1.2)
        self.f_crop.setChecked(True); self.f_nlm.setChecked(False); self.f_yadif.setChecked(False)
        self.x_bframes.setValue(8); self.x_badapt.setCurrentText("2: Full")
        self.x_lookahead.setValue(60); self.x_deblock.setText("-1,-1")
        self.x_merange.setValue(57); self.x_subme.setValue(7); self.x_me.setCurrentText("umh")
        self.x_ref.setValue(4); self.x_open_gop.setChecked(False)
        self.x_scenecut.setValue(40); self.x_keyint.setValue(250)
        self.x_hdr_mdcv.setText("G(13250,34500)B(7500,3000)R(34000,16000)WP(15635,16450)L(10000000,1)")
        self.x_hdr_cll.setText("1000,400")
        self._durata_sec = 0.0
        self._frame_totali = 0
        self.update_console("🔄 RESET")

    # ── ENCODING ─────────────────────────────────────────────────────────────
    def avvia_encoding(self):
        if self.in_corso: return
        self.in_corso = True
        self.btn_go.setEnabled(False); self.btn_stop.setEnabled(True)
        threading.Thread(target=self.processo_reale, daemon=True).start()

    def stop_encoding(self):
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            self.update_console("⏹ Interrotto.")
        self.in_corso = False
        self.btn_go.setEnabled(True); self.btn_stop.setEnabled(False)

    def on_fine(self, ok):
        self.in_corso = False
        self.btn_go.setEnabled(True); self.btn_stop.setEnabled(False)
        if ok:
            self.bar.setValue(1000)
            self.lbl_progress.setText(self.T("lbl_done"))
        else:
            self.bar.setValue(0)
            self.lbl_progress.setText(self.T("lbl_error"))

    # ── CONSOLE / PROGRESS ───────────────────────────────────────────────────
    def update_console(self, t):
        self.console.append(t)
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())

    def update_progresso(self, val):
        try:
            if val.startswith("frame:") and self._frame_totali > 0:
                # Progresso basato sui frame — affidabile su qualsiasi file
                frame_cur = int(val.split(":")[1])
                pct = min(frame_cur / self._frame_totali, 1.0)
                self.bar.setValue(int(pct * 1000))
                # Calcola tempo rimanente stimato
                sec_fatti = self._durata_sec * pct
                rimasto = max(self._durata_sec - sec_fatti, 0)
                rm, rs = divmod(int(rimasto), 60); rh, rm = divmod(rm, 60)
                hf = int(sec_fatti // 3600); mf = int((sec_fatti % 3600) // 60); sf = int(sec_fatti % 60)
                tot = f"{int(self._durata_sec//3600):02d}:{int((self._durata_sec%3600)//60):02d}:{int(self._durata_sec%60):02d}"
                self.lbl_progress.setText(
                    f"⏱  {hf:02d}:{mf:02d}:{sf:02d}  /  {tot}"
                    f"   —   {frame_cur:,} / {self._frame_totali:,} frame"
                    f"   —   ETA {rh:02d}:{rm:02d}:{rs:02d}")
            elif self._durata_sec > 0 and not val.startswith("frame:"):
                # Fallback su time= se disponibile
                p = val.strip().split(":")
                sec = float(p[0])*3600 + float(p[1])*60 + float(p[2])
                pct = min(sec/self._durata_sec, 1.0)
                self.bar.setValue(int(pct*1000))
        except Exception: pass

    # ── MOTORE FFMPEG ─────────────────────────────────────────────────────────
    def processo_reale(self):
        self._proc = None
        try:
            if not self.file_in:
                self.signals.fine.emit(False); return

            nome_base = os.path.splitext(os.path.basename(self.file_in))[0]
            out = os.path.join(self.output_dir or os.path.dirname(self.file_in),
                               nome_base + "_MASTERED.mkv")

            # Cropdetect
            crop_filter = ""
            if self.f_crop.isChecked():
                self.signals.log.emit(self.T("crop_detecting"))
                try:
                    cp = subprocess.run(
                        ["ffmpeg","-i",self.file_in,"-vf","cropdetect=24:16:0",
                         "-frames:v","500","-f","null","-"],
                        capture_output=True, text=True)
                    lines = [l for l in cp.stderr.splitlines() if "crop=" in l]
                    if lines:
                        cv = lines[-1].split("crop=")[-1].split()[0]
                        self.signals.log.emit(f"{self.T('crop_found')} {cv}")
                        crop_filter = f"crop={cv}"
                    else:
                        self.signals.log.emit(self.T("crop_none"))
                except Exception as e:
                    self.signals.log.emit(f"⚠️ cropdetect: {e}")

            # Filtri
            fc = []
            if self.f_yadif.isChecked(): fc.append("yadif=mode=1:parity=-1:deint=1")
            if crop_filter: fc.append(crop_filter)
            scale_map = {"3840x2160 (4K)":"scale=3840:2160","1920x1080 (FHD)":"scale=1920:1080","1280x720 (HD)":"scale=1280:720"}
            if self.f_scale.currentText() in scale_map:
                fc.append(f"{scale_map[self.f_scale.currentText()]}:flags={self.f_scale_algo.currentText()}")
            dn = self.f_dn.value()
            if self.f_nlm.isChecked(): fc.append(f"nlmeans=s={max(dn*2,1.0):.1f}:p=7:r=15")
            elif dn > 0: fc.append(f"hqdn3d={dn:.2f}:{dn:.2f}:{dn*3:.2f}:{dn*3:.2f}")
            sh = self.f_sh.value()
            if sh > 0: fc.append(f"unsharp=lx=5:ly=5:la={sh:.2f}:cx=3:cy=3:ca=0.0")
            gm = self.f_gamma.value(); sat = self.f_sat.value()
            if gm != 1.0 or sat != 1.0: fc.append(f"eq=gamma={gm:.3f}:saturation={sat:.3f}")
            if self.f_deband.isChecked():
                db = self.f_deband_str.value()
                fc.append(f"deband=1thr={db*0.01:.4f}:2thr={db*0.008:.4f}:3thr={db*0.008:.4f}:4thr={db*0.008:.4f}:range=22:direction=2:blur=1")
            vf = ",".join(fc) if fc else None

            # Encoder
            enc      = self.v_enc.currentText()
            rf       = self.v_rf.value()
            preset   = self.v_pre.currentText()
            bitdepth = self.v_bit.currentText()
            maxrate  = self.v_maxrate.value()
            bufsize  = self.v_bufsize.value()
            aq_map   = {"1: Standard":1,"2: Auto-Varianza":2,"3: Dark Scene":3}
            aq_mode  = aq_map.get(self.f_aq.currentText(),2)
            psy      = self.f_psy.value(); psycb = self.f_psycb.value()
            fps_map  = {"Originale (Source)":None,"23.976":"24000/1001","24":"24","25":"25","50":"50","60":"60"}
            fps      = fps_map.get(self.v_fps.currentText())
            range_map= {"Originale":None,"tv (Limited 16-235)":"tv","pc (Full 0-255)":"pc"}
            color_range = range_map.get(self.v_range.currentText())

            cmd = ["ffmpeg","-y","-i",self.file_in,"-map","0:v:0"]
            if vf: cmd += ["-vf", vf]
            cmd += ["-c:v", enc]

            if enc == "libx265":
                badapt_map = {"0: Off":0,"1: Fast":1,"2: Full":2}
                x265 = [
                    f"crf={rf}", f"preset={preset}",
                    f"aq-mode={aq_mode}", f"psy-rd={psy:.2f}", f"psy-rdoq={psycb:.2f}",
                    f"deblock={self.x_deblock.text().strip() or '-1,-1'}",
                    f"rc-lookahead={self.x_lookahead.value()}",
                    f"bframes={self.x_bframes.value()}",
                    f"b-adapt={badapt_map.get(self.x_badapt.currentText(),2)}",
                    f"me={self.x_me.currentText()}", f"merange={self.x_merange.value()}",
                    f"subme={self.x_subme.value()}", f"ref={self.x_ref.value()}",
                    f"scenecut={self.x_scenecut.value()}", f"keyint={self.x_keyint.value()}",
                    f"open-gop={'1' if self.x_open_gop.isChecked() else '0'}",
                ]
                th = self.x_threads.value()
                if th > 0: x265.append(f"pools={th}")
                if bitdepth == "10-bit (HDR)": x265 += ["profile=main10","high-tier=1"]
                if self.ck_hdr.isChecked():
                    x265 += ["colorprim=bt2020","colormatrix=bt2020nc","transfer=smpte2084",
                             "hdr-opt=1","repeat-headers=1",
                             f"master-display={self.x_hdr_mdcv.text().strip()}",
                             f"max-cll={self.x_hdr_cll.text().strip()}"]
                if maxrate > 0:
                    buf = bufsize if bufsize > 0 else maxrate*2
                    x265 += [f"vbv-maxrate={maxrate}",f"vbv-bufsize={buf}"]
                cmd += ["-x265-params",":".join(x265)]
                cmd += ["-pix_fmt","yuv420p10le" if bitdepth=="10-bit (HDR)" else "yuv420p"]

            elif enc == "libx264":
                cmd += ["-crf",str(int(rf)),"-preset",preset,
                        "-x264-params",f"aq-mode={aq_mode}:psy-rd={psy:.2f},0.10"]
                cmd += ["-pix_fmt","yuv420p"]

            elif enc == "hevc_vaapi":
                # VAAPI richiede: init dispositivo + upload filtro + formato
                # Inserisci PRIMA di -i il dispositivo vaapi
                cmd.insert(1, "-vaapi_device")
                cmd.insert(2, "/dev/dri/renderD128")
                # Aggiungi filtro hwupload prima dei filtri video
                if vf:
                    cmd = [c if c != vf else f"{vf},hwupload,format=vaapi" for c in cmd]
                else:
                    cmd += ["-vf", "hwupload,format=vaapi"]
                cmd += ["-qp", str(int(rf))]
                # VAAPI usa yuv420p per 8-bit o p010 per 10-bit
                if bitdepth == "10-bit (HDR)":
                    cmd += ["-pix_fmt", "p010le"]
                else:
                    cmd += ["-pix_fmt", "yuv420p"]

            elif enc == "hevc_nvenc":
                cmd += ["-qp", str(int(rf)), "-preset", "p4"]
                if bitdepth == "10-bit (HDR)":
                    cmd += ["-pix_fmt", "p010le"]
                else:
                    cmd += ["-pix_fmt", "yuv420p"]

            if fps: cmd += ["-r",fps]
            if color_range: cmd += ["-color_range",color_range]
            if self.ck_hdrcopy.isChecked(): cmd += ["-bsf:v","hevc_mp4toannexb","-map_chapters","0"]

            # Audio / Sub mapping
            bitrate_map = {
                "E-AC3 640k":  ("eac3","640k",None),
                "E-AC3 1536k": ("eac3","1536k",None),
                "AAC 256k":    ("aac","256k",None),
                "AAC 192k":    ("aac","192k","2"),
            }
            audio_out = 0; sub_out = 0
            for r in range(self.table.rowCount()):
                orig_id  = self.table.item(r,0).text() if self.table.item(r,0) else "0"
                tipo     = self.table.item(r,0).data(Qt.ItemDataRole.UserRole) if self.table.item(r,0) else ""
                cb       = self.table.cellWidget(r,5)
                azione   = cb.currentText() if cb else ""
                ck_def   = self.table.cellWidget(r,6)
                ck_for   = self.table.cellWidget(r,7)

                # Rimuovi / skip
                if self.T("aud_remove") in azione: continue

                if tipo == "AUDIO":
                    cmd += ["-map",f"0:{orig_id}"]
                    if self.T("aud_keep") in azione:
                        cmd += [f"-c:a:{audio_out}","copy"]
                    else:
                        # Estrai il formato dalla stringa "Converti → E-AC3 640k"
                        fmt_key = azione.split("→")[-1].strip() if "→" in azione else ""
                        if fmt_key in bitrate_map:
                            enc_a, br, ch = bitrate_map[fmt_key]
                            cmd += [f"-c:a:{audio_out}",enc_a,f"-b:a:{audio_out}",br,f"-ar:{audio_out}","48000"]
                            if ch: cmd += [f"-ac:{audio_out}",ch]
                    disp = [f for f in [
                        "default" if (ck_def and ck_def.isChecked()) else "",
                        "forced"  if (ck_for and ck_for.isChecked()) else ""
                    ] if f]
                    if disp: cmd += [f"-disposition:a:{audio_out}","+".join(disp)]
                    audio_out += 1

                elif tipo == "SUBTITLES":
                    cmd += ["-map",f"0:{orig_id}",f"-c:s:{sub_out}","copy"]
                    disp = [f for f in [
                        "default" if (ck_def and ck_def.isChecked()) else "",
                        "forced"  if (ck_for and ck_for.isChecked()) else ""
                    ] if f]
                    if disp: cmd += [f"-disposition:s:{sub_out}","+".join(disp)]
                    sub_out += 1

            if self.ck_web.isChecked():
                cmd += ["-movflags","+faststart","-avoid_negative_ts","make_zero"]
            cmd.append(out)

            if os.path.exists(out):
                self.signals.log.emit(f"{self.T('file_exists')} {os.path.basename(out)}")
            self.signals.log.emit("─"*55)
            self.signals.log.emit(f"{self.T('encoding_cmd')}  {' '.join(cmd[:6])} ...")
            self.signals.log.emit("─"*55)

            self._proc = subprocess.Popen(cmd,stderr=subprocess.STDOUT,
                                           stdout=subprocess.PIPE,text=True,bufsize=1)

            for line in self._proc.stdout:
                line = line.strip()
                if not line: continue
                if "frame=" in line:
                    # Usa i frame per il progresso — più affidabile del time=
                    try:
                        frame_val = line.split("frame=")[1].strip().split()[0]
                        if frame_val.isdigit():
                            self.signals.progresso.emit(f"frame:{frame_val}")
                    except Exception: pass
                    self.signals.log.emit(line)
                elif any(k in line for k in ("Error","error","Warning","warning")):
                    self.signals.log.emit(line)

            self._proc.wait()
            if self._proc.returncode == 0:
                self.signals.log.emit(f"\n{self.T('encoding_done')} {out}")
                self.signals.progresso.emit(f"frame:{self._frame_totali}")
                self.signals.fine.emit(True)
            else:
                self.signals.log.emit(self.T("encoding_err").format(self._proc.returncode))
                self.signals.fine.emit(False)

        except Exception as e:
            self.signals.log.emit(f"{self.T('encoding_crit')} {e}")
            self.signals.fine.emit(False)

    # ── DIALOGHI ─────────────────────────────────────────────────────────────
    def _show_manual(self):
        ManualDialog(self, lang=self._lang).exec()

    def _show_about(self):
        QMessageBox.about(self, "TitanEncode",
            "<h2 style='color:#4a9eff'>TitanEncode</h2>"
            "<b>HDR Video Mastering Suite</b><br><br>"
            "Version 1.0.0<br>"
            "License: GPL v3<br><br>"
            "Built with Python · PyQt6 · FFmpeg · x265<br><br>"
            "<i>Requires: ffmpeg, ffprobe, PyQt6</i>")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = TitanEncode()
    win.show()
    sys.exit(app.exec())
