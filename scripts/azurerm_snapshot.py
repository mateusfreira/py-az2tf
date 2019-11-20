# azurerm_snapshot
def azurerm_snapshot(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_snapshot"
    tcode="350-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST snapshot"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/snapshots"
        params = {'api-version': '2018-09-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')



            #suri=azr[i]["creationData"]["sourceUri"]
            #srid=azr[i]["creationData"]["sourceResourceId"]
            #said=azr[i]["creationData"]["storageAccountId"]
            try:
                co=azr[i]["properties"]["creationData"]["createOption"]
                fr.write('\t create_option = "' +  co + '"\n')
            except KeyError:
                pass


            try :
                sz=azr[i]["properties"]["diskSizeGb"]
                fr.write('\t disk_size_gb = "' +  sz + '"\n')
       
            #if suri" try :
            #    fr.write('\t source_uri = "' +  suri + '"\n')
            #fi
            #if srid" try :
            #    fr.write('\t source_resource_id = "' +  srid + '"\n')
            #fi
            #if said" try :
            #    fr.write('\t source_account_id = "' +  said + '"\n')
            #fi        
            except KeyError:
                pass


    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
