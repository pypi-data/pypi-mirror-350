from .ips import *



# to quick look at the patient info
def get_patient(kw=None,type_=None,thr=5,columns=["sampleid","patientid","birth","experimentator","consent form","first","res","type"]):
    def _get_patient(kw=None,type_=None):
        if "aml" in type_.lower():
            fpath=local_path(r'Q:\\IM\\AGLengerke\\Jeff\\Cell Bank\\AML Cells\\AML Data Collection Form.xlsx')
            sheet_name=1
            dir_aml=local_path(r"Q:\IM\AGLengerke\Lab\1_AML_Sample_Table\August_Updated_AML_Sample_Table.xlsx")
            
        else:
            fpath=local_path(r"Q:\IM\Klinik_IM2\Car-T-cells\JW_Tabelle aller CAR-T-cell Patienten und Proben.xlsx")
            sheet_name=0
        try: 
            df=fload(fpath=fpath,sheet_name=sheet_name,verbose=0)
        except Exception as e:
            print(e)
        print()
        if "aml" in type_.lower():
            name_lists=df.iloc[:,0].tolist()
            print("AML patients:")
        else:
            df["Name"]=df["Name"].apply(lambda x: str(x).strip().replace(" ",""))
            df["Geb."]=df["Geb."].apply(lambda x: str2date(str(x),fmt="%d.%m.%y"))
            name_lists=unique([n+"/"+d for n,d in zip(df["Name"], df["Geb."])], ascending=True )
            print("Car-T patients:")
            
        list_=[]
        for i  in name_lists: 
            if kw.lower() in str(i).lower():
                print(f"{i} => '{"A"+enpass(i,method="5d").upper()[:6]}'") 
                list_.append(i) 
        if "aml" in type_.lower(): 
            pat_id_=["A"+enpass(i,method="5d").upper()[:6] for i in name_lists] 
            pat_id_list=[] 
            for i,j in zip(name_lists, pat_id_): 
                if kw.upper() ==j:
                    print(f"{i} => '{j}'")
                    list_.append(f"{i} => '{j}'")
                    pat_id_list.append(j)  
        if 1 <= len(list_) <= thr: 
            if "aml" in type_.lower(): 
                print(f"\n\nfound {len(list_)}")
                df_aml = fload(dir_aml, sheet_name=0, header=1)
                idx_=1
                for name_ in list_:
                    if "=>" in name_:
                        name_=ssplit(name_,by=" =>")[0].strip()
                    print(f"{len(list_)}-{idx_}: {name_}")
                    if columns is None: 
                        display(df_aml.loc[df_aml["PatientID"]==("A"+enpass(name_,method="5d").upper()[:6])].iloc[:,:19])
                    else:
                        display(df_aml.loc[df_aml["PatientID"]==("A"+enpass(name_,method="5d").upper()[:6])].select(columns))
                    idx_+=1 
        return list_
    res=[]
    if kw is None:
        kw=input("input any related keyword:   , dateformat: %")
    kw=str(kw).replace(" ","").strip().lower()
    if type_ is None:
        for type_temp in ["aml","cart"]:
           res.extend(_get_patient(kw=kw,type_=type_temp))
    else:
        res.extend(_get_patient(kw=kw,type_=type_))
    return res