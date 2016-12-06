import sys
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    String,
    SmallInteger,
    types,
    func,
    ForeignKeyConstraint,
    Float,
    )

from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )
import re
from ...tools import (
    as_timezone,
    FixLength,
    )

from ...models import CommonModel
from ...models.pbb import pbbBase, pbbDBSession

KECAMATAN = [
    ('kd_propinsi', 2, 'N'),
    ('kd_dati2', 2, 'N'),
    ('kd_kecamatan', 3, 'N'),]
    
KELURAHAN = [
    ('kd_propinsi', 2, 'N'),
    ('kd_dati2', 2, 'N'),
    ('kd_kecamatan', 3, 'N'),
    ('kd_kelurahan', 3, 'N'),]
    

ARGS = {'extend_existing':True, 'autoload':True,
        'schema': pbbBase.pbb_schema}

class Propinsi(pbbBase, CommonModel):
    __tablename__  = 'ref_propinsi'
    __table_args__ = ARGS
    kd_propinsi = Column(String(2), primary_key=True)
    nm_propinsi = Column(String(30))
    
class Dati2(pbbBase, CommonModel):
    __tablename__  = 'ref_dati2'
    __table_args__ = (ForeignKeyConstraint(['kd_propinsi'], 
                                            ['ref_propinsi.kd_propinsi']),
                     ARGS,
                     )
    kd_propinsi = Column(String(2), primary_key=True)
    kd_dati2 = Column(String(2), primary_key=True)
    nm_dati2 = Column(String(30))
                     
class Kecamatan(pbbBase, CommonModel):
    __tablename__  = 'ref_kecamatan'
    __table_args__ = (ForeignKeyConstraint(['kd_propinsi','kd_dati2'], 
                                            ['ref_dati2.kd_propinsi', 'ref_dati2.kd_dati2']),
                      ARGS)
    kd_propinsi = Column(String(2), primary_key=True)
    kd_dati2 = Column(String(2), primary_key=True)
    kd_kecamatan = Column(String(2), primary_key=True)
    nm_kecamatan = Column(String(30))

class Kelurahan(pbbBase, CommonModel):
    __tablename__  = 'ref_kelurahan'
    __table_args__ = (ForeignKeyConstraint(['kd_propinsi','kd_dati2','kd_kecamatan'], 
                                            ['ref_kecamatan.kd_propinsi', 'ref_kecamatan.kd_dati2',
                                             'ref_kecamatan.kd_kecamatan']),
                     ARGS)
    kd_propinsi = Column(String(2), primary_key=True)
    kd_dati2 = Column(String(2), primary_key=True)
    kd_kecamatan = Column(String(2), primary_key=True)
    kd_kelurahan = Column(String(2), primary_key=True)
    nm_kelurahan = Column(String(30))
    no_kelurahn  = Column(Integer)
    kd_pos_kelurahan = Column(String(5))
    
    
class Kanwil(pbbBase, CommonModel):
    __tablename__  = 'ref_kanwil'
    __table_args__ = (ARGS)
    kd_kanwil = Column(String(2), primary_key=True)
    nm_kanwil = Column(String(30))
    al_kanwil = Column(String(50))
    kota_terbit_kanwil = Column(String(30))
    no_faksimili = Column(String(50))
    no_telpon = Column(String(50))
  
  
class Kantor(pbbBase, CommonModel):
    __tablename__  = 'ref_kantor'
    __table_args__ = (ForeignKeyConstraint(['kd_kanwil'], 
                                            ['ref_kanwil.kd_kanwil']),
                     ARGS)
    kd_kanwil = Column(String(2), primary_key=True)
    kd_kantor = Column(String(2), primary_key=True)
    nm_kantor = Column(String(30),)
    al_kantor = Column(String(50),)
    kota_terbit = Column(String(30),)
    no_faksimili = Column(String(50),)
    no_telpon = Column(String(50),)

class AdmKantor(pbbBase, CommonModel):
    __tablename__  = 'ref_adm_kantor'
    __table_args__ = (ForeignKeyConstraint(['kd_kanwil', 'kd_kantor'], 
                                            ['ref_kantor.kd_kanwil', 'ref_kantor.kd_kantor']),
                      ForeignKeyConstraint(['kd_propinsi', 'kd_dati2', 'kd_kecamatan'], 
                                            ['ref_kecamatan.kd_propinsi', 'ref_kecamatan.kd_dati2', 'ref_kecamatan.kd_kecamatan']),
                                            ARGS)
    kd_kanwil = Column(String(2), primary_key=True)
    kd_kantor = Column(String(2), primary_key=True)
    kd_propinsi = Column(String(2), primary_key=True)
    kd_dati2 = Column(String(2), primary_key=True)
    kd_kecamatan = Column(String(3), primary_key=True)

  
class Seksi(pbbBase, CommonModel):
    __tablename__  = 'ref_seksi'
    __table_args__ = (ARGS)
    kd_seksi = Column(String(2), primary_key=True)
    nm_seksi = Column(String(75),)
    no_srt_seksi = Column(String(2),)
    kode_surat_1 = Column(String(5),)
    kode_surat_2 = Column(String(5),)

class JnsSektor(pbbBase, CommonModel):
    __tablename__  = 'ref_jns_sektor'
    __table_args__ = (ARGS)
    kd_sektor = Column(String(2), primary_key=True)
    nm_sektor = Column(String(75),)

class JnsPembetulan(pbbBase, CommonModel):
    __tablename__  = 'ref_jns_pembetulan'
    __table_args__ = (ARGS)
    kd_pembetulan = Column(String(2), primary_key=True)
    nm_pembetulan = Column(String(100),)
    

class JnsPelayanan(pbbBase, CommonModel):
    __tablename__  = 'ref_jns_pelayanan'
    __table_args__ = (ARGS)
    kd_jns_pelayanan = Column(String(2), primary_key=True)
    nm_jenis_pelayanan = Column(String(50),)

class Buku(pbbBase, CommonModel):
    __tablename__  = 'ref_buku'
    __table_args__ = (ARGS)
    thn_awal = Column(String(4), primary_key=True)
    thn_akhir = Column(String(4), primary_key=True)
    kd_buku = Column(String(1), primary_key=True)
    nilai_min_buku = Column(Float)
    nilai_max_buku = Column(Float)

class Jabatan(pbbBase, CommonModel):
    __tablename__  = 'ref_jabatan'
    __table_args__ = (ARGS)
    kd_jabatan = Column(String(2), primary_key=True)
    nm_jabatan = Column(String(30),)
    singkatan_jabatan = Column(String(30),)
    
class Jpb(pbbBase, CommonModel):
    __tablename__  = 'ref_jpb'
    __table_args__ = (ARGS)
    kd_jpb = Column(String(2), primary_key=True)
    nm_jpb = Column(String(50),)

  