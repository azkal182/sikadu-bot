import requests
from bs4 import BeautifulSoup
import json

class Sikadu:
  data = {
      'nim' : '02.15.0.0320',
      'passuser' : 'isticaem',
      'an_sec' : '12345', 
      'angka1' : '12345',
      'kirim' : 'L.O.G.I.N'
    }
  def __init__(self):
    self.s = requests.session()
    data = {
      'nim' : '02.15.0.0320',
      'passuser' : 'isticaem',
      'an_sec' : '12345', 
      'angka1' : '12345',
      'kirim' : 'L.O.G.I.N'
    }
    r = self.s.post('http://sikadu.unwahas.ac.id/BU/', data = data)
    #return r
  def soup(self, url):
    req = self.s.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    #print(url)
    return soup


  def search(self, nim):
    #requests.session()
    #r = self.s.get('http://sikadu.unwahas.ac.id/SU_admin/m2_mhs.php?mng=aktkrs&kdmhs=21106011089')
    raw = self.soup('http://sikadu.unwahas.ac.id/SU_admin/m2_mhs.php?mng=aktkrs&kdmhs='+nim)
    data1 = raw.find('table')
    data2 = raw.find_all('table')[1]
    krs = data2.find_all('td')[10]
    link_krs = krs.find('a').get('href')
    sikadu = data2.find_all('td')[11]
    link_sikadu = sikadu.find('a').get('href')
    uas = data2.find_all('td')[12]
    link_uas = uas.find('a').get('href')
    uts = data2.find_all('td')[13]
    link_uts = uts.find('a').get('href')
    reset = data2.find_all('td')[14]
    link_reset = reset.find('a').get('href')
    
    nama = data1.find_all('b')[0].text
    nim = data1.find_all('b')[1].text
    passwd = data1.find_all('b')[2].text
    kelas = data1.find_all('b')[3].text
    angkatan = data1.find_all('b')[4].text
    ip_lalu = data1.find_all('b')[5].text
    lis = []
    res = {
      'name' : nama,
      'nim' : nim,
      'password' : passwd,
      'kelas' : kelas,
      'angkatan' : angkatan,
      'ip_lalu' : ip_lalu,
      'account': {
        'krs' : krs.text,
        'link_krs' : link_krs,
        'sikadu' : sikadu.text,
        'link_sikadu' : link_sikadu,
        'uas' : uas.text,
        'link_uas' : link_uas,
        'uts' : uts.text,
        'link_uts' : link_uts,
        'reset' : reset,
        'link_reset' : link_reset
      }
    }
    lis.append(res)
    return res
