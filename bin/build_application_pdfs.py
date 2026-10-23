"""Rebuild the public application PDFs. Run from any directory.

Dependencies: reportlab, PyYAML. Uses _data/cv.yml and authentic project images.
Font lookup supports macOS system fonts and Linux Liberation/DejaVu fonts.
"""
from pathlib import Path
from io import BytesIO
from xml.sax.saxutils import escape
import yaml
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/pdf'
IMG = ROOT / 'assets/img/projects'
EXTRA = ROOT / 'assets/img/portfolio'
DATA = yaml.safe_load((ROOT / '_data/cv.yml').read_text())['cv']
INK, MUTED, PURPLE, TEAL = map(colors.HexColor, ['#202A35', '#566477', '#7041A3', '#287C8E'])
BG, LINE = map(colors.HexColor, ['#F5F7FA', '#D7DEE8'])

def fonts():
    roots = [Path('/System/Library/Fonts/Supplemental'), Path('/usr/share/fonts/truetype/liberation2'), Path('/usr/share/fonts/truetype/dejavu')]
    options = {'Body': ['Arial.ttf', 'LiberationSans-Regular.ttf', 'DejaVuSans.ttf'],
               'BodyBold': ['Arial Bold.ttf', 'LiberationSans-Bold.ttf', 'DejaVuSans-Bold.ttf'],
               'Serif': ['Times New Roman.ttf', 'LiberationSerif-Regular.ttf', 'DejaVuSerif.ttf'],
               'SerifBold': ['Times New Roman Bold.ttf', 'LiberationSerif-Bold.ttf', 'DejaVuSerif-Bold.ttf']}
    for name, files in options.items():
        p = next((r / f for r in roots for f in files if (r / f).exists()), None)
        if p is None: raise RuntimeError('Install Liberation fonts or supply the documented macOS fonts.')
        pdfmetrics.registerFont(TTFont(name, str(p)))
    pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold')
    pdfmetrics.registerFontFamily('Serif', normal='Serif', bold='SerifBold')

def clean(s):
    return str(s).replace('–', '-').replace('—', '-').replace('‑', '-').replace('’', "'")

def markup(s):
    return escape(clean(s))

def build_cv():
    body = ParagraphStyle('cvbody', fontName='Serif', fontSize=9.5, leading=12.3, textColor=INK, spaceAfter=4)
    title = ParagraphStyle('cvtitle', parent=body, fontName='SerifBold', fontSize=26, leading=29, alignment=TA_CENTER, spaceAfter=5)
    contact = ParagraphStyle('cvcontact', parent=body, alignment=TA_CENTER, fontSize=9.3, leading=12, spaceAfter=8)
    heading = ParagraphStyle('cvheading', parent=body, fontName='SerifBold', fontSize=13, leading=16, spaceBefore=8, spaceAfter=6, borderWidth=0.4, borderColor=LINE, borderPadding=3)
    sub = ParagraphStyle('cvsub', parent=body, fontName='SerifBold', fontSize=10.3, leading=12.7, spaceBefore=4)
    bullet = ParagraphStyle('cvbullet', parent=body, leftIndent=10, firstLineIndent=-8, spaceAfter=3)
    story = [Paragraph('Shuwei Zhao', title), Paragraph('+852-9572-0915 | shwzhao3@gmail.com | <link href="https://www.linkedin.com/in/shuwei-zhao-5116382b1/">LinkedIn</link> | <link href="https://shuwei-zhao.github.io/">Website</link>', contact)]
    def para(s, style=body): return Paragraph(s, style)
    def section(s): story.append(para(s, heading))
    def experience(e):
        project = e['summary'].split('. ', 1)[-1].split('; advisor')[0].split('; supervisor')[0]
        dates = clean(f"{e['start_date']} - {e['end_date']}")
        advisor = e['summary'].split('; ')[-1]
        group = [para(markup(project), sub), para(f"{markup(e['position'])} | {markup(e['company'])} | {dates}<br/>{markup(advisor)}")]
        group += [para('- '+markup(x), bullet) for x in e['highlights']]
        story.append(KeepTogether(group))
    section('Education')
    for e in DATA['sections']['Education']:
        story += [para(markup(e['institution'])+' | '+clean(e['start_date'])+' - '+clean(e['end_date']), sub), para(markup(e['studyType']+' in '+e['area'])+' | '+markup(e['location']))]
        story += [para('- '+markup(x), bullet) for x in e['highlights']]
    section('Research Interests')
    story.append(para('Cable-driven mechanisms and actuation systems; wearable robotics and supernumerary robotic limbs; soft, compliant, and continuum robots; sensing, control, and experimental characterization.'))
    section('Research Experience')
    for e in DATA['sections']['Research Experience'][:3]: experience(e)
    story.append(PageBreak())
    section('Research Experience (continued)')
    for e in DATA['sections']['Research Experience'][3:]: experience(e)
    section('Publications')
    for i, p in enumerate(DATA['sections']['Publications'], 1):
        story.append(para(f"[{i}] {markup(p['summary'].split('. Accepted')[0])}. <b>{markup(p['title'])}</b>. {markup(p['publisher'])}, 2026. "+('Accepted. Shuwei Zhao and Ruizhou Zhao contributed equally.' if i==1 else 'Accepted at IEEE ICRA 2026. Author manuscript available on arXiv: <link href="https://arxiv.org/abs/2602.06207">2602.06207</link>. Ruizhou Zhao and Yichen Chu contributed equally.')))
    section('Awards')
    for a in DATA['sections']['Awards']:
        detail = ' | '+markup(a['awarder']) if a.get('awarder') else ''
        if a.get('summary'): detail += '; '+markup(a['summary'])
        story.append(para('<b>'+markup(a['title'])+'</b> ('+markup(a['date'])+')'+detail))
    section('Skills')
    for s in DATA['sections']['Skills']: story.append(para('<b>'+markup(s['name'])+':</b> '+markup(s['keywords'])))
    section('Selected Course Project')
    e=DATA['sections']['Selected Course Project'][0]
    story += [para(markup(e['title'])+' | October 2024 - January 2025', sub), para('Course Project | The Chinese University of Hong Kong | Advisor: Ms. Lai Yin NGAN.')]
    story += [para('- '+markup(x), bullet) for x in e['highlights']]
    def footer(c, doc):
        c.setFont('Serif',8);c.setFillColor(MUTED);c.drawString(38,24,'Shuwei Zhao | Curriculum Vitae');c.drawRightString(557,24,str(doc.page))
    doc=SimpleDocTemplate(str(OUT/'Shuwei_Zhao_CV.pdf'),pagesize=(595.28,841.89),leftMargin=38,rightMargin=38,topMargin=31,bottomMargin=36,title='Shuwei Zhao - Curriculum Vitae',author='Shuwei Zhao')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

class Portfolio:
    def __init__(self):
        self.c=canvas.Canvas(str(OUT/'Shuwei_Zhao_Research_Portfolio.pdf'),pagesize=(960,540))
        self.c.setTitle('Shuwei Zhao - Robotic Mechanisms, Actuation & System Integration');self.c.setAuthor('Shuwei Zhao');self.page=0
    def text(self,s,x,y,w,size=12,bold=False,color=INK,leading=None):
        p=Paragraph(s,ParagraphStyle('p',fontName='BodyBold' if bold else 'Body',fontSize=size,leading=leading or size*1.32,textColor=color))
        _,h=p.wrap(w,1000);p.drawOn(self.c,x,540-y-h);return h
    def line(self,y):self.c.setStrokeColor(LINE);self.c.setLineWidth(.7);self.c.line(38,540-y,922,540-y)
    def image(self,name,x,y,w,h,extra=False):
        f=(EXTRA if extra else IMG)/name
        source=Image.open(f).convert('RGB');source.thumbnail((2400,2400),Image.Resampling.LANCZOS)
        encoded=BytesIO();source.save(encoded,format='JPEG',quality=93,subsampling=0);encoded.seek(0)
        im=ImageReader(encoded);iw,ih=im.getSize();scale=min(w/iw,h/ih);dw,dh=iw*scale,ih*scale
        self.c.setFillColor(colors.white);self.c.roundRect(x,540-y-h,w,h,5,fill=1,stroke=0)
        self.c.drawImage(im,x+(w-dw)/2,540-y-h+(h-dh)/2,dw,dh,mask='auto')
    def start(self,label,title,subtitle=''):
        if self.page:self.c.showPage()
        self.page+=1;self.c.setFillColor(BG);self.c.rect(0,0,960,540,fill=1,stroke=0)
        self.text(label.upper(),38,27,884,9,True,PURPLE)
        self.text(title,38,49,884,24,True,leading=27)
        if subtitle:self.text(subtitle,38,83,884,10,color=MUTED)
        self.line(504);self.text('Shuwei Zhao | Research Portfolio | 2026',38,513,750,8,color=MUTED);self.text(f'{self.page:02d}',900,511,25,9,True,PURPLE)
    def block(self,label,body,x,y,w,size=12):
        h=self.text(label.upper(),x,y,w,9,True,PURPLE)
        return self.text(body,x,y+h+7,w,size)+h+7
    def save(self):self.c.save()

def build_portfolio():
    p=Portfolio()
    p.start('Research Portfolio','Robotic Mechanisms, Actuation &amp; System Integration')
    p.text('Shuwei Zhao',38,112,420,25,True)
    p.text('B.Eng. Candidate in Electronic Engineering<br/>The Chinese University of Hong Kong<br/>Expected graduation: May 2027',38,151,410,12,color=MUTED)
    p.text('Selected projects in mechanical design, embedded control, magnetic and soft actuation, and experimental validation.',38,224,410,15)
    p.block('Research interests','Cable-driven mechanisms, compliant robotics, and wearable systems.',38,310,410,15)
    p.block('PhD applications','Fall 2027<br/>Hardware development - actuation - sensing - system integration',38,405,410,12)
    p.image('xjtu-catheter-accumulator-crop.jpg',483,115,439,250)
    p.text('My contribution at XJTU: the translating-pulley catheter accumulator, mechanical assembly, Arduino firmware, and PC motion-control interface. Real photograph, cropped.',483,377,439,10,color=MUTED)
    p.text('CUHK | Xi’an Jiaotong University | ETH Zürich',483,445,439,12,True,TEAL)

    p.start('Project 01 | XJTU | July-August 2026','Motorized Catheter Management for Industrial Inspection','Research Assistant | Prof. Qiji Ze’s group, Xi’an Jiaotong University')
    p.image('xjtu-catheter-accumulator-crop.jpg',38,120,562,178)
    p.image('xjtu-catheter-management.jpg',38,315,280,151)
    p.text('Laboratory platform: robot-assisted magnetic manipulation and the complete industrial-inspection system were team infrastructure. The original photograph provides system context.',334,324,266,11,color=MUTED)
    p.block('Mechanism design','Designed and built a translating-pulley catheter accumulator; approximately ΔL ≈ 2Δx length compensation. Fusion 360 / SolidWorks assembly with a 120-mm guide pulley, 608 bearings, MGN12H carriage, T8 lead screw, and 3D-printed interfaces.',624,120,298,11)
    p.block('Complete control chain','Python/Tkinter → USB serial → Arduino UNO → TB6600 → stepper-driven stage. Calibration, jogging, fixed-distance motion, adjustable speed/acceleration, travel limits, and a communication watchdog.',624,278,298,11)
    p.text('My contribution: the translating-pulley catheter accumulator, its mechanical assembly, Arduino firmware, and PC motion-control interface.',38,480,562,9,color=MUTED)
    p.text('Foundation for further work in robotic mechanisms, motion transmission, and actuation systems.',624,444,298,11,True,TEAL)

    p.start('Project 02 | CUHK | June-July 2026','Magnetically Steerable Micro-Camera Catheter','Co-first author | Accepted at ICBIR 2026 | Advisor: Prof. Hongliang Ren')
    p.image('bronchial-catheter-concept.png',38,115,278,340)
    p.image('bronchial-prototype.png',340,122,278,170,True)
    p.image('bronchial-fabrication.png',638,122,284,170,True)
    p.text('Prototype structure',340,302,278,10,True,TEAL);p.text('Composite preparation, magnetization, and distal assembly',638,302,284,10,True,TEAL)
    p.block('My contribution','Designed and fabricated the millimeter-scale catheter; integrated the LED micro-camera, 0.2-mm nitinol support wire, heat-shrink encapsulation, and hard-magnetic Ecoflex cuff. Developed insertion-force and steering-characterization setups and contributed to manuscript and figure preparation.',340,346,582,13)
    p.text('Design concept for bronchial-tree phantom navigation',38,465,278,9,color=MUTED)
    p.text('Shuwei Zhao†, Ruizhou Zhao†, Zhiqing Tang, Wenchao Yue, Hongliang Ren. †Shuwei Zhao and Ruizhou Zhao contributed equally.',340,465,582,9,color=MUTED)

    p.start('Project 02 | CUHK | Experimental evaluation','Magnetic Steering and Forward-Looking Imaging','Bronchial-tree phantom experiments | Manual external permanent-magnet actuation')
    p.image('bronchial-catheter-validation.png',38,115,585,335)
    p.block('Insertion characterization','Characterized insertion force under dry and saline-wetted conditions.',648,120,274,12)
    p.block('Steering and navigation','Evaluated multidirectional magnetic steering and forward-looking imaging in a bronchial-tree phantom, including primary and secondary bifurcations.',648,220,274,12)
    p.block('Scope of evidence','Benchtop phantom evaluation. Further work includes controlled magnetic actuation, visual feedback, and repeated quantitative navigation tests.',648,354,274,11)
    p.text('Magnetically assisted branch redirection. Image sequence reproduced from existing experimental materials.',38,465,585,10,color=MUTED)

    p.start('Project 03 | ETH Zürich | March-June 2026','Soft Miniaturized Intraductal Imaging Catheter','Multi-Scale Robotics Lab | Prof. Bradley Nelson | Semester-project grade: 5.5/6.0')
    p.image('eth-intraductal-catheter.jpg',38,122,275,207)
    p.image('eth-force-platform.jpg',337,122,275,207)
    p.image('eth-phantom.jpg',636,122,286,207,True)
    p.block('Flexible prototypes','Designed and fabricated flexible imaging catheter prototypes using 0.5-mm and 0.7-mm nitinol support wires, investigating flexibility, pushability, and insertion resistance. These are support-wire diameters.',38,350,275,11)
    p.block('Calibrated force measurement','Built and calibrated a four-load-cell platform with Arduino/Python acquisition. The reported analysis used 10 selected trials from 20 recorded manual trials per condition and included a 1.1-mm rigid reference.',337,350,275,11)
    p.block('Experimental comparison','Compared support and surface configurations. Fabricated a silicone breast-duct phantom and evaluated imaging with external illumination, including a porcine-blood condition. Results are limited to simplified benchtop models.',636,350,286,11)

    p.start('Project 04 | CUHK | June-August 2025','Kirigami Capsule for Gastrointestinal Biopsy','Contributing author | Accepted at IEEE ICRA 2026 | Advisor: Prof. Hongliang Ren')
    p.image('kirigami-mechanism.png',38,118,424,233,True)
    p.image('kirigami-control.png',486,118,436,233,True)
    p.block('System integration and ex vivo validation','Contributed to iterative assembly, ex vivo porcine experiments, quantitative analysis, and validation writing. Team prototype: 17-mm diameter and 22-mm length.',38,370,424,11)
    p.block('Motor control and angular calibration','Developed motor-control electronics and Arduino pulse-control logic. Built an angular calibration platform (approximately 18.1 degrees per pulse; R² = 0.99).',486,370,436,11)
    p.text('Ruizhou Zhao†, Yichen Chu†, Shuwei Zhao, Wenchao Yue, Raymond Shing-Yan Tang, Hongliang Ren. †Ruizhou Zhao and Yichen Chu contributed equally.',38,449,884,9,color=MUTED)
    p.text('Author manuscript: arxiv.org/abs/2602.06207. Ex vivo prototype evaluation does not establish clinical safety.',38,476,884,9,color=MUTED)
    p.c.linkURL('https://arxiv.org/abs/2602.06207',(38,45,620,66),relative=0)

    p.start('Research development | Current work and future interests','From Hardware Integration to Robotic Assistance')
    p.block('Pneumatic Soft Jumping Robot','Designed and fabricated a double-layer spherical-cap silicone actuator and Arduino pneumatic control for benchtop jumping. Developed geometric models and investigated actuator radius and opening angle, deformation, and elastic-energy storage. Ongoing since September 2025.',38,126,414,13)
    p.block('Existing work | imaging and delivery catheter','My current work focuses on integrating the imaging module, magnetic steering components, and an independent drug-delivery channel within a flexible catheter. Prototype development is ongoing, and experimental validation is planned.',38,320,414,13)
    p.block('Intended PhD research directions','I am interested in extending my experience in mechanism design, actuation, and embedded control toward cable-driven and wearable robotic systems. Potential directions include modular actuation interfaces, lightweight compliant mechanisms, and sensing and control for physical assistance.',493,126,429,15)
    p.text('These are intended PhD research directions rather than completed projects.',493,348,429,14,True,PURPLE)
    p.text('I aim to deepen my expertise in modeling, control, and learning-based methods while building on my hardware and system-integration experience.',493,410,429,12,color=MUTED)
    p.save()

if __name__=='__main__':
    OUT.mkdir(exist_ok=True,parents=True);fonts();build_cv();build_portfolio()
    print('Rebuilt CV and Research Portfolio in assets/pdf/.')
