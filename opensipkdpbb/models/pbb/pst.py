import sys
from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
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
    literal_column,
    )
from sqlalchemy.orm import aliased

from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )
import re
from ...tools import as_timezone, FixLength

from ...models import CommonModel
from ...models.pbb import pbbBase, pbbDBSession
#from pbb_ref_wilayah import Kelurahan, Kecamatan, Dati2, KELURAHAN, KECAMATAN

# class PstJenis(pbbBase, CommonModel):
    # __tablename__  = 'ref_jns_pelayanan'
    # __table_args__ = {'extend_existing':True, 'autoload':True,
                      # 'schema': pbbBase.pbb_schema}

ARGS = {'extend_existing':True,  #'autoload':True,
        'schema': pbbBase.pbb_schema}
                      
class PstBerkasKirim(pbbBase, CommonModel):
    __tablename__  = 'berkas_kirim'
    __table_args__ = ARGS
    kd_kanwil = Column(String(2), primary_key = True)
    kd_kantor = Column(String(2), primary_key = True)
    thn_pelayanan = Column(String(4), primary_key = True)
    bundel_pelayanan = Column(String(4), primary_key = True)
    no_urut_pelayanan = Column(String(3), primary_key = True)
    kd_propinsi_pemohon = Column(String(2), primary_key = True)
    kd_dati2_pemohon = Column(String(2), primary_key = True)
    kd_kecamatan_pemohon = Column(String(3), primary_key = True)
    kd_kelurahan_pemohon = Column(String(3), primary_key = True)
    kd_blok_pemohon = Column(String(3), primary_key = True)
    no_urut_pemohon = Column(String(4), primary_key = True)
    kd_jns_op_pemohon = Column(String(1), primary_key = True)
    kd_seksi = Column(String(2), primary_key = True)
    thn_agenda_kirim = Column(String(4), primary_key = True)
    no_agenda_kirim = Column(String(30), primary_key = True)
    tgl_kirim =Column(DateTime(timezone=False))
    nip_pengirim_berkas = Column(String(18))


class PstBerkasTerima(pbbBase, CommonModel):
    __tablename__  = 'berkas_terima'
    __table_args__ = ARGS
    kd_kanwil = Column(String(2), primary_key = True)
    kd_kantor = Column(String(2), primary_key = True)
    thn_pelayanan = Column(String(4), primary_key = True)
    bundel_pelayanan = Column(String(4), primary_key = True)
    no_urut_pelayanan = Column(String(3), primary_key = True)
    kd_propinsi_pemohon = Column(String(2), primary_key = True)
    kd_dati2_pemohon = Column(String(2), primary_key = True)
    kd_kecamatan_pemohon = Column(String(3), primary_key = True)
    kd_kelurahan_pemohon = Column(String(3), primary_key = True)
    kd_blok_pemohon = Column(String(3), primary_key = True)
    no_urut_pemohon = Column(String(4), primary_key = True)
    kd_jns_op_pemohon = Column(String(1), primary_key = True)
    kd_seksi = Column(String(2), primary_key = True)
    thn_agenda_kirim = Column(String(4), primary_key = True)
    no_agenda_kirim = Column(String(30), primary_key = True)
    kd_seksi_terima = Column(String(2),)
    tgl_terima = Column(DateTime(timezone=False))
    nip_penerima_berkas = Column(String(18),)
  
class PstPermohonan(pbbBase, CommonModel):
    __tablename__  = 'pst_permohonan'
    __table_args__ = ARGS
    kd_kanwil = Column(String(2), primary_key = True)
    kd_kantor = Column(String(2), primary_key = True)
    thn_pelayanan = Column(String(4), primary_key = True)
    bundel_pelayanan = Column(String(4), primary_key = True)
    no_urut_pelayanan = Column(String(3), primary_key = True)
    no_srt_permohonan = Column(String(30),)
    tgl_surat_permohonan = Column(Date)
    nama_pemohon = Column(String(30),)
    alamat_pemohon = Column(String(40),)
    keterangan_pst = Column(String(75),)
    catatan_pst = Column(String(75),)
    status_kolektif = Column(String(1))
    tgl_terima_dokumen_wp = Column(DateTime(timezone=False))
    tgl_perkiraan_selesai = Column(Date)
    nip_penerima = Column(String(18),)
  
    @classmethod
    def get_by_nopel(cls, r):
        return pbbDBSession.query(cls).\
                             filter(cls.kd_kanwil==r['kd_kanwil'],
                                       cls.kd_kantor==r['kd_kantor'],
                                       cls.thn_pelayanan==r['thn_pelayanan'], 
                                       cls.bundel_pelayanan==r['bundel_pelayanan'],
                                       cls.no_urut_pelayanan==r['no_urut_pelayanan'],).\
                             first()

class PstLampiran(pbbBase, CommonModel):
    __tablename__  = 'pst_lampiran'
    __table_args__ = (ForeignKeyConstraint(['kd_kanwil', 'kd_kantor', 'thn_pelayanan', 
                                            'bundel_pelayanan', 'no_urut_pelayanan'], 
                                            ['pst_permohonan.kd_kanwil', 
                                             'pst_permohonan.kd_kantor', 
                                             'pst_permohonan.thn_pelayanan', 
                                             'pst_permohonan.bundel_pelayanan', 
                                             'pst_permohonan.no_urut_pelayanan']),
                     ARGS,
                     )
    kd_kanwil = Column(String(2), primary_key = True)
    kd_kantor = Column(String(2), primary_key = True)
    thn_pelayanan = Column(String(4), primary_key = True)
    bundel_pelayanan = Column(String(4), primary_key = True)
    no_urut_pelayanan = Column(String(3), primary_key = True)
    l_permohonan = Column(Integer)
    l_surat_kuasa = Column(Integer)
    l_ktp_wp = Column(Integer)
    l_sertifikat_tanah = Column(Integer)
    l_sppt = Column(Integer)
    l_imb = Column(Integer)
    l_akte_jual_beli = Column(Integer)
    l_sk_pensiun = Column(Integer)
    l_sppt_stts = Column(Integer)
    l_stts = Column(Integer)
    l_sk_pengurangan = Column(Integer)
    l_sk_keberatan = Column(Integer)
    l_skkp_pbb = Column(Integer)
    l_spmkp_pbb = Column(Integer)
    l_lain_lain = Column(Integer)
    l_sket_tanah = Column(Integer)
    l_sket_lurah = Column(Integer)
    l_npwpd = Column(Integer)
    l_penghasilan = Column(Integer)
    l_cagar = Column(Integer)
  
    @classmethod
    def get_by_nopel(cls, r):
        return pbbDBSession.query(cls).\
                             filter(cls.kd_kanwil==r['kd_kanwil'],
                                       cls.kd_kantor==r['kd_kantor'],
                                       cls.thn_pelayanan==r['thn_pelayanan'], 
                                       cls.bundel_pelayanan==r['bundel_pelayanan'],
                                       cls.no_urut_pelayanan==r['no_urut_pelayanan'],).\
                             first()

    
class PstDetail(pbbBase, CommonModel):
    __tablename__  = 'pst_detail'
    __table_args__ = (ForeignKeyConstraint(['kd_kanwil', 'kd_kantor', 'thn_pelayanan', 
                                            'bundel_pelayanan', 'no_urut_pelayanan'], 
                                            ['pst_permohonan.kd_kanwil', 
                                             'pst_permohonan.kd_kantor', 
                                             'pst_permohonan.thn_pelayanan', 
                                             'pst_permohonan.bundel_pelayanan', 
                                             'pst_permohonan.no_urut_pelayanan']),
    
                      ARGS,
                      )
    kd_kanwil = Column(String(2), primary_key = True)
    kd_kantor = Column(String(2), primary_key = True)
    thn_pelayanan = Column(String(4), primary_key = True)
    bundel_pelayanan = Column(String(4), primary_key = True)
    no_urut_pelayanan = Column(String(3), primary_key = True)
    kd_propinsi_pemohon = Column(String(2), primary_key = True)
    kd_dati2_pemohon = Column(String(2), primary_key = True)
    kd_kecamatan_pemohon = Column(String(3), primary_key = True)
    kd_kelurahan_pemohon = Column(String(3), primary_key = True)
    kd_blok_pemohon = Column(String(3), primary_key = True)
    no_urut_pemohon = Column(String(4), primary_key = True)
    kd_jns_op_pemohon = Column(String(1), primary_key = True)
    kd_jns_pelayanan = Column(String(2),)
    thn_pajak_permohonan = Column(String(4),)
    nama_penerima = Column(String(30))
    catatan_penyerahan = Column(String(75),)
    status_selesai = Column(Integer)
    tgl_selesai = Column(Date)
    kd_seksi_berkas = Column(String(2),)
    tgl_penyerahan = Column(Date)
    nip_penyerah = Column(String(18),) 
    @classmethod
    def get_by_nopel(cls, r):
        return pbbDBSession.query(cls).\
                             filter(cls.kd_kanwil            ==r['kd_kanwil'],
                                    cls.kd_kanwil            ==r['kd_kanwil'], 
                                    cls.kd_kantor            ==r['kd_kantor'], 
                                    cls.thn_pelayanan        ==r['thn_pelayanan'], 
                                    cls.bundel_pelayanan     ==r['bundel_pelayanan'], 
                                    cls.no_urut_pelayanan    ==r['no_urut_pelayanan'], 
                                    cls.kd_propinsi_pemohon  ==r['kd_propinsi_pemohon'], 
                                    cls.kd_dati2_pemohon     ==r['kd_dati2_pemohon'], 
                                    cls.kd_kecamatan_pemohon ==r['kd_kecamatan_pemohon'], 
                                    cls.kd_kelurahan_pemohon ==r['kd_kelurahan_pemohon'], 
                                    cls.kd_blok_pemohon      ==r['kd_blok_pemohon'], 
                                    cls.no_urut_pemohon      ==r['no_urut_pemohon'], 
                                    cls.kd_jns_op_pemohon    ==r['kd_jns_op_pemohon'], ).\
                             first()
    @classmethod
    def get_position(cls, r):
        return pbbDBSession.query(cls.kd_kanwil, cls.kd_kantor, cls.thn_pelayanan, 
                    cls.bundel_pelayanan, cls.no_urut_pelayanan, 
                    cls.kd_propinsi_pemohon, cls.kd_dati2_pemohon, cls.kd_kecamatan_pemohon, 
                    cls.kd_kelurahan_pemohon, cls.kd_blok_pemohon, cls.no_urut_pemohon, 
                    cls.kd_jns_op_pemohon, cls.kd_jns_pelayanan, cls.thn_pajak_permohonan, 
                    cls.nama_penerima, cls.catatan_penyerahan, cls.status_selesai, 
                    cls.tgl_selesai, cls.kd_seksi_berkas, cls.tgl_penyerahan, cls.nip_penyerah,
                    Seksi.kd_seksi, Seksi.nm_seksi).\
                             filter(cls.kd_kanwil            ==r['kd_kanwil'],
                                    cls.kd_kanwil            ==r['kd_kanwil'], 
                                    cls.kd_kantor            ==r['kd_kantor'], 
                                    cls.thn_pelayanan        ==r['thn_pelayanan'], 
                                    cls.bundel_pelayanan     ==r['bundel_pelayanan'], 
                                    cls.no_urut_pelayanan    ==r['no_urut_pelayanan'], 
                                    cls.kd_propinsi_pemohon  ==r['kd_propinsi_pemohon'], 
                                    cls.kd_dati2_pemohon     ==r['kd_dati2_pemohon'], 
                                    cls.kd_kecamatan_pemohon ==r['kd_kecamatan_pemohon'], 
                                    cls.kd_kelurahan_pemohon ==r['kd_kelurahan_pemohon'], 
                                    cls.kd_blok_pemohon      ==r['kd_blok_pemohon'], 
                                    cls.no_urut_pemohon      ==r['no_urut_pemohon'], 
                                    cls.kd_jns_op_pemohon    ==r['kd_jns_op_pemohon'], 
                                    cls.kd_seksi_berkas      == Seksi.kd_seksi)

                                    
    @classmethod
    def get_tracking(cls, r):
        SeksiAlias = aliased(Seksi, name='seksi_alias')
        return pbbDBSession.query(cls.kd_kanwil, cls.kd_kantor, cls.thn_pelayanan, 
                    cls.bundel_pelayanan, cls.no_urut_pelayanan, 
                    cls.kd_propinsi_pemohon, cls.kd_dati2_pemohon, cls.kd_kecamatan_pemohon, 
                    cls.kd_kelurahan_pemohon, cls.kd_blok_pemohon, cls.no_urut_pemohon, 
                    cls.kd_jns_op_pemohon,
                    PstBerkasKirim.kd_seksi,
                    PstBerkasKirim.thn_agenda_kirim,
                    PstBerkasKirim.no_agenda_kirim,
                    PstBerkasKirim.tgl_kirim,
                    PstBerkasTerima.kd_seksi_terima,
                    PstBerkasTerima.tgl_terima,
                    Seksi.nm_seksi.label('pengirim'),
                    SeksiAlias.nm_seksi.label('penerima')).\
                             filter(cls.kd_kanwil            ==r['kd_kanwil'],
                                    cls.kd_kanwil            ==r['kd_kanwil'], 
                                    cls.kd_kantor            ==r['kd_kantor'], 
                                    cls.thn_pelayanan        ==r['thn_pelayanan'], 
                                    cls.bundel_pelayanan     ==r['bundel_pelayanan'], 
                                    cls.no_urut_pelayanan    ==r['no_urut_pelayanan'], 
                                    cls.kd_propinsi_pemohon  ==r['kd_propinsi_pemohon'], 
                                    cls.kd_dati2_pemohon     ==r['kd_dati2_pemohon'], 
                                    cls.kd_kecamatan_pemohon ==r['kd_kecamatan_pemohon'], 
                                    cls.kd_kelurahan_pemohon ==r['kd_kelurahan_pemohon'], 
                                    cls.kd_blok_pemohon      ==r['kd_blok_pemohon'], 
                                    cls.no_urut_pemohon      ==r['no_urut_pemohon'], 
                                    cls.kd_jns_op_pemohon    ==r['kd_jns_op_pemohon'],
                                    
                                    cls.kd_kanwil            ==PstBerkasKirim.kd_kanwil, 
                                    cls.kd_kantor            ==PstBerkasKirim.kd_kantor, 
                                    cls.thn_pelayanan        ==PstBerkasKirim.thn_pelayanan, 
                                    cls.bundel_pelayanan     ==PstBerkasKirim.bundel_pelayanan, 
                                    cls.no_urut_pelayanan    ==PstBerkasKirim.no_urut_pelayanan, 
                                    cls.kd_propinsi_pemohon  ==PstBerkasKirim.kd_propinsi_pemohon, 
                                    cls.kd_dati2_pemohon     ==PstBerkasKirim.kd_dati2_pemohon, 
                                    cls.kd_kecamatan_pemohon ==PstBerkasKirim.kd_kecamatan_pemohon, 
                                    cls.kd_kelurahan_pemohon ==PstBerkasKirim.kd_kelurahan_pemohon, 
                                    cls.kd_blok_pemohon      ==PstBerkasKirim.kd_blok_pemohon, 
                                    cls.no_urut_pemohon      ==PstBerkasKirim.no_urut_pemohon, 
                                    cls.kd_jns_op_pemohon    ==PstBerkasKirim.kd_jns_op_pemohon,
                                    PstBerkasKirim.kd_seksi  ==Seksi.kd_seksi,
                                    PstBerkasKirim.kd_kanwil            ==PstBerkasTerima.kd_kanwil, 
                                    PstBerkasKirim.kd_kantor            ==PstBerkasTerima.kd_kantor, 
                                    PstBerkasKirim.thn_pelayanan        ==PstBerkasTerima.thn_pelayanan, 
                                    PstBerkasKirim.bundel_pelayanan     ==PstBerkasTerima.bundel_pelayanan, 
                                    PstBerkasKirim.no_urut_pelayanan    ==PstBerkasTerima.no_urut_pelayanan, 
                                    PstBerkasKirim.kd_propinsi_pemohon  ==PstBerkasTerima.kd_propinsi_pemohon, 
                                    PstBerkasKirim.kd_dati2_pemohon     ==PstBerkasTerima.kd_dati2_pemohon, 
                                    PstBerkasKirim.kd_kecamatan_pemohon ==PstBerkasTerima.kd_kecamatan_pemohon, 
                                    PstBerkasKirim.kd_kelurahan_pemohon ==PstBerkasTerima.kd_kelurahan_pemohon, 
                                    PstBerkasKirim.kd_blok_pemohon      ==PstBerkasTerima.kd_blok_pemohon, 
                                    PstBerkasKirim.no_urut_pemohon      ==PstBerkasTerima.no_urut_pemohon, 
                                    PstBerkasKirim.kd_jns_op_pemohon    ==PstBerkasTerima.kd_jns_op_pemohon,
                                    PstBerkasKirim.kd_seksi             ==PstBerkasTerima.kd_seksi        ,
                                    PstBerkasKirim.thn_agenda_kirim     ==PstBerkasTerima.thn_agenda_kirim,
                                    PstBerkasKirim.no_agenda_kirim      ==PstBerkasTerima.no_agenda_kirim ,
                                    
                                    PstBerkasTerima.kd_seksi_terima      ==SeksiAlias.kd_seksi,
                                    )
                                    
class PstDataOpBaru(pbbBase, CommonModel):
    __tablename__  = 'pst_data_op_baru'
    __table_args__ = (ForeignKeyConstraint(['kd_kanwil', 'kd_kantor', 'thn_pelayanan', 
                                            'bundel_pelayanan', 'no_urut_pelayanan'], 
                                            ['pst_permohonan.kd_kanwil', 
                                             'pst_permohonan.kd_kantor', 
                                             'pst_permohonan.thn_pelayanan', 
                                             'pst_permohonan.bundel_pelayanan', 
                                             'pst_permohonan.no_urut_pelayanan']),
                     ARGS,
                     )
    kd_kanwil = Column(String(2), primary_key = True)
    kd_kantor = Column(String(2), primary_key = True)
    thn_pelayanan = Column(String(4), primary_key = True)
    bundel_pelayanan = Column(String(4), primary_key = True)
    no_urut_pelayanan = Column(String(3), primary_key = True)
    kd_propinsi_pemohon = Column(String(2), primary_key = True)
    kd_dati2_pemohon = Column(String(2), primary_key = True)
    kd_kecamatan_pemohon = Column(String(3), primary_key = True)
    kd_kelurahan_pemohon = Column(String(3), primary_key = True)
    kd_blok_pemohon = Column(String(3), primary_key = True)
    no_urut_pemohon = Column(String(4), primary_key = True)
    kd_jns_op_pemohon = Column(String(1), primary_key = True)
    nama_wp_baru = Column(String(30),)
    letak_op_baru = Column(String(35),)
    
    @classmethod
    def get_by_nopel(cls, r):
        return pbbDBSession.query(cls).\
                             filter(cls.kd_kanwil            ==r['kd_kanwil'],
                                    cls.kd_kanwil            ==r['kd_kanwil'], 
                                    cls.kd_kantor            ==r['kd_kantor'], 
                                    cls.thn_pelayanan        ==r['thn_pelayanan'], 
                                    cls.bundel_pelayanan     ==r['bundel_pelayanan'], 
                                    cls.no_urut_pelayanan    ==r['no_urut_pelayanan'], 
                                    cls.kd_propinsi_pemohon  ==r['kd_propinsi_pemohon'],
                                    cls.kd_dati2_pemohon     ==r['kd_dati2_pemohon'], 
                                    cls.kd_kecamatan_pemohon ==r['kd_kecamatan_pemohon'], 
                                    cls.kd_kelurahan_pemohon ==r['kd_kelurahan_pemohon'], 
                                    cls.kd_blok_pemohon      ==r['kd_blok_pemohon'], 
                                    cls.no_urut_pemohon      ==r['no_urut_pemohon'], 
                                    cls.kd_jns_op_pemohon    ==r['kd_jns_op_pemohon'], ).\
                             first()
                             
class PstPengurangan(pbbBase, CommonModel):
    __tablename__  = 'pst_permohonan_pengurangan'
    __table_args__ = (ForeignKeyConstraint(['kd_kanwil', 'kd_kantor', 'thn_pelayanan', 
                                            'bundel_pelayanan', 'no_urut_pelayanan'], 
                                            ['pst_permohonan.kd_kanwil', 
                                             'pst_permohonan.kd_kantor', 
                                             'pst_permohonan.thn_pelayanan', 
                                             'pst_permohonan.bundel_pelayanan', 
                                             'pst_permohonan.no_urut_pelayanan']),
                      ARGS,)
    kd_kanwil = Column(String(2), primary_key = True)
    kd_kantor = Column(String(2), primary_key = True)
    thn_pelayanan = Column(String(4), primary_key = True)
    bundel_pelayanan = Column(String(4), primary_key = True)
    no_urut_pelayanan = Column(String(3), primary_key = True)
    kd_propinsi_pemohon = Column(String(2), primary_key = True)
    kd_dati2_pemohon = Column(String(2), primary_key = True)
    kd_kecamatan_pemohon = Column(String(3), primary_key = True)
    kd_kelurahan_pemohon = Column(String(3), primary_key = True)
    kd_blok_pemohon = Column(String(3), primary_key = True)
    no_urut_pemohon = Column(String(4), primary_key = True)
    kd_jns_op_pemohon = Column(String(1), primary_key = True)
    jns_pengurangan = Column(String(1),)
    pct_permohonan_pengurangan = Column(Integer)
  
    @classmethod
    def get_by_nopel(cls, r):
        return pbbDBSession.query(cls).\
                             filter(cls.kd_kanwil            ==r['kd_kanwil'],
                                    cls.kd_kanwil            ==r['kd_kanwil'], 
                                    cls.kd_kantor            ==r['kd_kantor'], 
                                    cls.thn_pelayanan        ==r['thn_pelayanan'], 
                                    cls.bundel_pelayanan     ==r['bundel_pelayanan'], 
                                    cls.no_urut_pelayanan    ==r['no_urut_pelayanan'], 
                                    cls.kd_propinsi_pemohon  ==r['kd_propinsi_pemohon'],
                                    cls.kd_dati2_pemohon     ==r['kd_dati2_pemohon'], 
                                    cls.kd_kecamatan_pemohon ==r['kd_kecamatan_pemohon'], 
                                    cls.kd_kelurahan_pemohon ==r['kd_kelurahan_pemohon'], 
                                    cls.kd_blok_pemohon      ==r['kd_blok_pemohon'], 
                                    cls.no_urut_pemohon      ==r['no_urut_pemohon'], 
                                    cls.kd_jns_op_pemohon    ==r['kd_jns_op_pemohon'], ).\
                             first()
                             
class MaxUrutPstOl(pbbBase, CommonModel):
    __tablename__  = 'max_urut_pst_ol'
    __table_args__ = ARGS
    kd_kanwil = Column(String(2), primary_key=True)          
    kd_kantor = Column(String(2), primary_key=True)
    thn_pelayanan = Column(String(4))           
    bundel_pelayanan = Column(String(4))
    no_urut_pelayanan = Column(String(3))

    @classmethod
    def query_data(cls):
        return pbbDBSession.query(cls)
    
    @classmethod
    def get_nopel(cls, request):
        settings = request.registry.settings
        
        thn_pelayanan = datetime.now().strftime('%Y')
        row = pbbDBSession.query(cls).first()
        if not row:
            row = cls()
            row.kd_kanwil = settings['pbb_kd_kanwil']
            row.kd_kantor = settings['pbb_kd_kantor']
            row.thn_pelayanan = thn_pelayanan
            row.bundel_pelayanan = '9000'
            row.no_urut_pelayanan = '000'
            
        if row.thn_pelayanan!=thn_pelayanan:
            row.thn_pelayanan = thn_pelayanan
            row.bundel_pelayanan = '9000'
            row.no_urut_pelayanan = '000'
            
        bundel_pelayanan = int(row.bundel_pelayanan)
        no_urut_pelayanan = int(row.no_urut_pelayanan)
        if no_urut_pelayanan == 999:
            bundel_pelayanan +=1
            no_urut_pelayanan = 1
        else:    
            no_urut_pelayanan += 1
            
        row.thn_pelayanan = thn_pelayanan
        row.bundel_pelayanan = str(bundel_pelayanan).zfill(4)
        row.no_urut_pelayanan = str(no_urut_pelayanan).zfill(3)
        pbbDBSession.add(row)
        pbbDBSession.flush()
        return (row.kd_kanwil, row.kd_kantor, row.thn_pelayanan, row.bundel_pelayanan, row.no_urut_pelayanan)
        
