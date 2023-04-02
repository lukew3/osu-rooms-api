from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

cookies = {
    'PS_DEVICEFEATURES': 'width:1920 height:1080 pixelratio:1 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0',
    'hcwebprd11-15000-PORTAL-PSJSESSIONID': 'KXRDj1iRW1joc_11Y55MepW2VoLaiUnv!-1602213654',
    'ExpirePage': 'https://courses.osu.edu/psp/csosuct/',
    'PS_LOGINLIST': 'https://courses.osu.edu/csosuct',
    'PS_TOKENEXPIRE': '2_Apr_2023_22:05:58_GMT',
    'PS_TOKEN': 'qwAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4AgQg4AC4AMQAwABT8RlSEoXpSOOzrCXmk5jlFG6wVXWsAAAAFAFNkYXRhX3icHYhLDkBAFATLJ05g5Q6EMSLWE+yM+Kydxb0cTs+8pLur3gvkWZok2i8lXuXw3ByczMrDKgt0Ucxs0nKXLfIHJ/LKjTW0GHpqrY1t1J24EQ9qG3nSP2TUlx/bNQ7O',
    'PS_TokenSite': 'https://courses.osu.edu/psp/csosuct/?hcwebprd12-15000-PORTAL-PSJSESSIONID',
    'SignOnDefault': '',
    'PS_LASTSITE': 'https://courses.osu.edu/psp/csosuct/',
    'ps_theme': 'node:CAMP portal:EMPLOYEE theme_id:OSU_TANGERINE_FL css:DEFAULT_THEME_FLUID css_f:OSU_FLUID_FLUID accessibility:N formfactor:3 piamode:2',
    'psback': '%22%22url%22%3A%22https%3A%2F%2Fcourses.osu.edu%2Fpsp%2Fcsosuct%2FEMPLOYEE%2FPUB%2Fc%2FOSR_CUSTOM_MENU.OSR_ROOM_MATRIX.GBL%3Fpage%3DOSR_ROOM_MATRIX%22%20%22label%22%3A%22Room%20Matrix%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcourses.osu.edu%2Fpsc%2Fcsosuct%2FEMPLOYEE%2FPUB%22%22',
    'hcwebprd12-15000-PORTAL-PSJSESSIONID': 'WNtEAT3BDVm7NLasHPo_QTWqHS6ZN6fg!-1167031497',
    'https%3a%2f%2fcourses.osu.edu%2fpsp%2fcsosuct%2femployee%2fcamp%2frefresh': 'list: %3ftab%3dos_facstaff_erp|%3frp%3dos_facstaff_erp|%3ftab%3dremoteunifieddashboard|%3frp%3dremoteunifieddashboard',
    'NSC_NX-DTPTV-DPVSTFT-TTM-WT': 'ffffffff839aa4b145525d5f4f58455e445a4a4206ab',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://courses.osu.edu',
    'Connection': 'keep-alive',
    'Referer': 'https://courses.osu.edu/psc/csosuct/EMPLOYEE/PUB/c/OSR_CUSTOM_MENU.OSR_ROOM_MATRIX.GBL?PortalActualURL=https%3a%2f%2fcourses.osu.edu%2fpsc%2fcsosuct%2fEMPLOYEE%2fPUB%2fc%2fOSR_CUSTOM_MENU.OSR_ROOM_MATRIX.GBL&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fcourses.osu.edu%2fpsp%2fcsosuct%2f&PortalURI=https%3a%2f%2fcourses.osu.edu%2fpsc%2fcsosuct%2f&PortalHostNode=CAMP&NoCrumbs=yes&PortalKeyStruct=yes',
    # 'Cookie': 'PS_DEVICEFEATURES=width:1920 height:1080 pixelratio:1 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; hcwebprd11-15000-PORTAL-PSJSESSIONID=KXRDj1iRW1joc_11Y55MepW2VoLaiUnv!-1602213654; ExpirePage=https://courses.osu.edu/psp/csosuct/; PS_LOGINLIST=https://courses.osu.edu/csosuct; PS_TOKENEXPIRE=2_Apr_2023_22:05:58_GMT; PS_TOKEN=qwAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4AgQg4AC4AMQAwABT8RlSEoXpSOOzrCXmk5jlFG6wVXWsAAAAFAFNkYXRhX3icHYhLDkBAFATLJ05g5Q6EMSLWE+yM+Kydxb0cTs+8pLur3gvkWZok2i8lXuXw3ByczMrDKgt0Ucxs0nKXLfIHJ/LKjTW0GHpqrY1t1J24EQ9qG3nSP2TUlx/bNQ7O; PS_TokenSite=https://courses.osu.edu/psp/csosuct/?hcwebprd12-15000-PORTAL-PSJSESSIONID; SignOnDefault=; PS_LASTSITE=https://courses.osu.edu/psp/csosuct/; ps_theme=node:CAMP portal:EMPLOYEE theme_id:OSU_TANGERINE_FL css:DEFAULT_THEME_FLUID css_f:OSU_FLUID_FLUID accessibility:N formfactor:3 piamode:2; psback=%22%22url%22%3A%22https%3A%2F%2Fcourses.osu.edu%2Fpsp%2Fcsosuct%2FEMPLOYEE%2FPUB%2Fc%2FOSR_CUSTOM_MENU.OSR_ROOM_MATRIX.GBL%3Fpage%3DOSR_ROOM_MATRIX%22%20%22label%22%3A%22Room%20Matrix%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcourses.osu.edu%2Fpsc%2Fcsosuct%2FEMPLOYEE%2FPUB%22%22; hcwebprd12-15000-PORTAL-PSJSESSIONID=WNtEAT3BDVm7NLasHPo_QTWqHS6ZN6fg!-1167031497; https%3a%2f%2fcourses.osu.edu%2fpsp%2fcsosuct%2femployee%2fcamp%2frefresh=list: %3ftab%3dos_facstaff_erp|%3frp%3dos_facstaff_erp|%3ftab%3dremoteunifieddashboard|%3frp%3dremoteunifieddashboard; NSC_NX-DTPTV-DPVSTFT-TTM-WT=ffffffff839aa4b145525d5f4f58455e445a4a4206ab',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

data = 'ICAJAX=1&ICNAVTYPEDROPDOWN=1&ICType=Panel&ICElementNum=0&ICStateNum=4&ICAction=DERIVED_CLASS_S_SSR_REFRESH_CAL&ICModelCancel=0&ICXPos=0&ICYPos=0&ResponsetoDiffFrame=-1&TargetFrameName=None&FacetPath=None&ICFocus=&ICSaveWarningFilter=0&ICChanged=-1&ICSkipPending=0&ICAutoSave=0&ICResubmit=0&ICSID=JAJSGNiahVEK%2BqmMiwIh7gAgfEAf%2FRerxO%2B4MUY2drM%3D&ICActionPrompt=true&ICBcDomData=C~UnknownValue~EMPLOYEE~PUB~OSR_CUSTOM_MENU.OSR_ROOM_MATRIX.GBL~OSR_ROOM_MATRIX~Room%20Matrix~UnknownValue~UnknownValue~https%3A%2F%2Fcourses.osu.edu%2Fpsp%2Fcsosuct%2FEMPLOYEE%2FPUB%2Fc%2FOSR_CUSTOM_MENU.OSR_ROOM_MATRIX.GBL%3FPortalKeyStruct%3Dyes~UnknownValue&ICPanelName=&ICFind=&ICAddCount=&ICAppClsData=&OSR_DERIVED_RM_FACILITY_ID=DL0369&DERIVED_CLASS_S_START_DT=03%2F27%2F2023&DERIVED_CLASS_S_MEETING_TIME_START=8%3A00AM&DERIVED_CLASS_S_MEETING_TIME_END=10%3A00PM&OSR_DERIVED_RM_START_DT=&OSR_DERIVED_RM_END_DT=&DERIVED_CLASS_S_MONDAY_LBL$30$$chk=Y&DERIVED_CLASS_S_MONDAY_LBL$30$=Y&DERIVED_CLASS_S_THURSDAY_LBL$chk=Y&DERIVED_CLASS_S_THURSDAY_LBL=Y&DERIVED_CLASS_S_SUNDAY_LBL$chk=Y&DERIVED_CLASS_S_SUNDAY_LBL=Y&DERIVED_CLASS_S_TUESDAY_LBL$chk=Y&DERIVED_CLASS_S_TUESDAY_LBL=Y&DERIVED_CLASS_S_FRIDAY_LBL$chk=Y&DERIVED_CLASS_S_FRIDAY_LBL=Y&DERIVED_CLASS_S_SHOW_AM_PM$chk=Y&DERIVED_CLASS_S_SHOW_AM_PM=Y&OSR_DERIVED_RM_OSR_SHOW_ROOM$chk=Y&OSR_DERIVED_RM_OSR_SHOW_ROOM=Y&DERIVED_CLASS_S_WEDNESDAY_LBL$chk=Y&DERIVED_CLASS_S_WEDNESDAY_LBL=Y&DERIVED_CLASS_S_SATURDAY_LBL$chk=Y&DERIVED_CLASS_S_SATURDAY_LBL=Y&DERIVED_CLASS_S_SSR_DISP_TITLE$chk=N&OSR_DERIVED_RM_OSR_SHOW_EVENTS$chk=Y&OSR_DERIVED_RM_OSR_SHOW_EVENTS=Y'

response = requests.post(
    'https://courses.osu.edu/psc/csosuct/EMPLOYEE/PUB/c/OSR_CUSTOM_MENU.OSR_ROOM_MATRIX.GBL',
    cookies=cookies,
    headers=headers,
    data=data,
)

with open('a.html', 'w') as f:
    f.write(str(response.content))

if __name__ == '__main__':
    app.run()
