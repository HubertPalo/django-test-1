from ftplib import FTP
class CameraService:

    def upload_photo(self, file, name):
        
        # content_type = 'image/jpeg'
        # response = "POST API and you have uploaded a {} file".format(content_type) + " called {}".format(file_uploaded)
        # response = "dir {}, dict {}".format(dir(file_uploaded), file_uploaded.__dict__)
        
        session = FTP(host='maonamata.com.br', user='mnmdev@maonamata.com.br', passwd='mnmDev2021')
        # response = session.pwd()
        session.storbinary('STOR ' + name, file)
        #session.cwd('./../../public_html/pipe1/trapassets/trap1test/')
        session.quit()