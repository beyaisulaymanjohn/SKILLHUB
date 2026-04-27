#!/usr/bin/env python3
"""
GamSkillHub - Comprehensive Business Strategy & Market Analysis Report
"""
import os, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, CondPageBreak
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ─── FONT REGISTRATION ───
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSansBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Carlito', '/usr/share/fonts/truetype/english/Carlito-Regular.ttf'))
pdfmetrics.registerFont(TTFont('CarlitoBold', '/usr/share/fonts/truetype/english/Carlito-Bold.ttf'))
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSansBold')
registerFontFamily('LiberationSerif', normal='LiberationSerif', bold='LiberationSerifBold')
registerFontFamily('Carlito', normal='Carlito', bold='CarlitoBold')

# ─── COLOR PALETTE ───
ACCENT = colors.HexColor('#5528da')
TEXT_PRIMARY = colors.HexColor('#191b1c')
TEXT_MUTED = colors.HexColor('#858d91')
BG_SURFACE = colors.HexColor('#d9dde0')
BG_PAGE = colors.HexColor('#eef1f2')

TABLE_HEADER_COLOR = ACCENT
TABLE_HEADER_TEXT = colors.white
TABLE_ROW_EVEN = colors.white
TABLE_ROW_ODD = BG_SURFACE

# ─── STYLES ───
styles = getSampleStyleSheet()

cover_title_style = ParagraphStyle(
    name='CoverTitle', fontName='LiberationSerif', fontSize=38,
    leading=46, alignment=TA_LEFT, textColor=TEXT_PRIMARY, spaceAfter=12
)
cover_sub_style = ParagraphStyle(
    name='CoverSub', fontName='Carlito', fontSize=16,
    leading=22, alignment=TA_LEFT, textColor=TEXT_MUTED, spaceAfter=6
)
cover_meta_style = ParagraphStyle(
    name='CoverMeta', fontName='Carlito', fontSize=12,
    leading=18, alignment=TA_LEFT, textColor=TEXT_MUTED
)

h1_style = ParagraphStyle(
    name='H1', fontName='LiberationSerif', fontSize=22,
    leading=28, alignment=TA_LEFT, textColor=ACCENT,
    spaceBefore=18, spaceAfter=12
)
h2_style = ParagraphStyle(
    name='H2', fontName='LiberationSerif', fontSize=16,
    leading=22, alignment=TA_LEFT, textColor=TEXT_PRIMARY,
    spaceBefore=14, spaceAfter=8
)
h3_style = ParagraphStyle(
    name='H3', fontName='LiberationSerif', fontSize=13,
    leading=18, alignment=TA_LEFT, textColor=TEXT_PRIMARY,
    spaceBefore=10, spaceAfter=6
)
body_style = ParagraphStyle(
    name='Body', fontName='LiberationSerif', fontSize=10.5,
    leading=17, alignment=TA_JUSTIFY, textColor=TEXT_PRIMARY,
    spaceBefore=0, spaceAfter=6
)
bullet_style = ParagraphStyle(
    name='Bullet', fontName='LiberationSerif', fontSize=10.5,
    leading=17, alignment=TA_LEFT, textColor=TEXT_PRIMARY,
    leftIndent=24, bulletIndent=12, spaceBefore=2, spaceAfter=2,
    bulletFontName='LiberationSerif', bulletFontSize=10.5
)
callout_style = ParagraphStyle(
    name='Callout', fontName='LiberationSerif', fontSize=10.5,
    leading=17, alignment=TA_LEFT, textColor=TEXT_PRIMARY,
    leftIndent=18, rightIndent=18, spaceBefore=8, spaceAfter=8,
    backColor=colors.HexColor('#f0eef8'), borderPadding=10
)
header_cell_style = ParagraphStyle(
    name='HeaderCell', fontName='LiberationSerif', fontSize=10,
    leading=14, alignment=TA_CENTER, textColor=colors.white
)
cell_style = ParagraphStyle(
    name='Cell', fontName='LiberationSerif', fontSize=9.5,
    leading=14, alignment=TA_LEFT, textColor=TEXT_PRIMARY
)
cell_center_style = ParagraphStyle(
    name='CellCenter', fontName='LiberationSerif', fontSize=9.5,
    leading=14, alignment=TA_CENTER, textColor=TEXT_PRIMARY
)
caption_style = ParagraphStyle(
    name='Caption', fontName='Carlito', fontSize=9,
    leading=13, alignment=TA_CENTER, textColor=TEXT_MUTED,
    spaceBefore=3, spaceAfter=6
)

# ─── HELPER FUNCTIONS ───
def h1(text):
    return Paragraph(f'<b>{text}</b>', h1_style)

def h2(text):
    return Paragraph(f'<b>{text}</b>', h2_style)

def h3(text):
    return Paragraph(f'<b>{text}</b>', h3_style)

def p(text):
    return Paragraph(text, body_style)

def bullet(text):
    return Paragraph(f'<bullet>&bull;</bullet> {text}', bullet_style)

def callout(text):
    return Paragraph(f'<b>Key Insight:</b> {text}', callout_style)

def make_table(headers, rows, col_widths=None):
    """Create a styled table with Paragraph cells."""
    available = A4[0] - 2*inch
    data = []
    header_row = [Paragraph(f'<b>{h}</b>', header_cell_style) for h in headers]
    data.append(header_row)
    for row in rows:
        data.append([Paragraph(str(c), cell_style) for c in row])
    if col_widths is None:
        n = len(headers)
        col_widths = [available / n] * n
    else:
        total = sum(col_widths)
        if total < available * 0.85:
            scale = (available * 0.92) / total
            col_widths = [w * scale for w in col_widths]
    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), TABLE_HEADER_TEXT),
        ('GRID', (0, 0), (-1, -1), 0.5, TEXT_MUTED),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        bg = TABLE_ROW_EVEN if i % 2 == 1 else TABLE_ROW_ODD
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t

# ─── TOC TEMPLATE ───
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

def add_heading(text, style, level=0):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph(f'<a name="{key}"/>{text}', style)
    p.bookmark_name = text
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def add_major_section(text, style):
    available_height = A4[1] - 2*inch
    threshold = available_height * 0.15
    return [
        CondPageBreak(threshold),
        add_heading(f'<b>{text}</b>', style, level=0),
    ]

# ─── PAGE TEMPLATE ───
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Carlito', 9)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawCentredString(A4[0] / 2, 30, f'Page {doc.page}')
    canvas.drawString(inch, 30, 'GamSkillHub')
    canvas.restoreState()

# ─── BUILD DOCUMENT ───
output_path = '/home/z/my-project/download/GamSkillHub_Business_Strategy_Report.pdf'

doc = TocDocTemplate(
    output_path,
    pagesize=A4,
    topMargin=1.0*inch,
    bottomMargin=0.8*inch,
    leftMargin=1.0*inch,
    rightMargin=1.0*inch,
    title='GamSkillHub - Business Strategy & Market Analysis',
    author='GamSkillHub',
    subject='Comprehensive business strategy and market analysis for The Gambia'
)

story = []

# ══════════════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════════════
story.append(Spacer(1, 120))
story.append(Paragraph('<b>GamSkillHub</b>', cover_title_style))
story.append(Spacer(1, 12))
story.append(Paragraph('Comprehensive Business Strategy<br/>&amp; Market Analysis Report', cover_sub_style))
story.append(Spacer(1, 30))

# Decorative line
line_table = Table([['']], colWidths=[200], rowHeights=[3])
line_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), ACCENT),
    ('LINEBELOW', (0,0), (-1,-1), 3, ACCENT),
]))
story.append(line_table)
story.append(Spacer(1, 30))

story.append(Paragraph('Gambia\'s Premier Skilled Worker Platform', cover_sub_style))
story.append(Spacer(1, 8))
story.append(Paragraph('Market Research | Monetization Strategy | Payment Integration<br/>Partnership Roadmap | Go-To-Market Plan', cover_meta_style))
story.append(Spacer(1, 60))
story.append(Paragraph('Prepared for: GamSkillHub Founding Team<br/>Date: April 2026<br/>Version: 1.0 | Confidential', cover_meta_style))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ══════════════════════════════════════════════════════════════
story.append(Paragraph('<b>Table of Contents</b>', h1_style))
story.append(Spacer(1, 12))

toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle(name='TOC1', fontName='LiberationSerif', fontSize=12, leftIndent=20, leading=20, spaceBefore=6),
    ParagraphStyle(name='TOC2', fontName='LiberationSerif', fontSize=10.5, leftIndent=40, leading=18, spaceBefore=2),
]
story.append(toc)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# 1. EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('1. Executive Summary', h1_style))
story.append(Spacer(1, 8))
story.append(p(
    'GamSkillHub is positioned to become The Gambia\'s leading digital marketplace for skilled workers, '
    'connecting tradespeople with homeowners, businesses, and government institutions. The platform addresses '
    'a critical market failure: the disconnect between a growing pool of informal skilled labor and the surging '
    'demand from a booming construction and real estate sector. With GDP growth at 5.7% in 2024, a housing '
    'deficit exceeding 128,000 units, and youth unemployment at 41.5%, the opportunity for a technology-driven '
    'solution is both enormous and urgent.'
))
story.append(p(
    'The Gambian economy is undergoing a significant transformation. The OIC Summit infrastructure investments, '
    'including a $50 million road network and airport modernization, have catalyzed real estate development '
    'across the Kombo area. Major projects by Sablux ($200M investment), Brufut Heights, and TUI Blue Tamala '
    'hotel are reshaping demand for skilled trades. Simultaneously, 81% of Gambian employment remains informal, '
    'meaning millions of skilled workers operate without visibility, reliable income streams, or professional '
    'development pathways.'
))
story.append(p(
    'This report presents a comprehensive analysis of the Gambian market landscape, identifies key client '
    'segments across government, banking, hospitality, and telecommunications sectors, and outlines detailed '
    'monetization strategies. It also addresses the critical question of payment infrastructure, evaluating '
    'integration opportunities with Wave, Modem Pay, PawaPay, and the newly launched BANTABA 2.0 real-time '
    'payment switch. Finally, it maps out a phased go-to-market plan with clear milestones, target segments, '
    'and partnership strategies to ensure sustainable revenue growth.'
))

story.append(callout(
    'The addressable market for skilled services in The Gambia is estimated at over D5 billion annually, '
    'driven by construction, facility maintenance, and hospitality sector demand. GamSkillHub can capture '
    '5-15% of this market within 3-5 years through a commission-based model combined with B2B subscriptions.'
))

# ══════════════════════════════════════════════════════════════
# 2. THE GAMBIAN SKILLED LABOR MARKET LANDSCAPE
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('2. The Gambian Skilled Labor Market Landscape', h1_style))

story.append(h2('2.1 Economic Overview and Employment Trends'))
story.append(p(
    'The Gambia\'s economy has shown robust growth in recent years, posting a 5.7% GDP expansion in 2024, '
    'with projections of 5.3% growth through 2025-2026 according to IMF and World Bank assessments. This growth '
    'has been driven primarily by agriculture, tourism, construction, and remittances from the diaspora. The '
    'construction sector alone contributed 4.4% to GDP in 2024, a figure that reflects the intensive '
    'infrastructure development undertaken for the OIC Summit and ongoing urbanization in the Greater Banjul '
    'area, particularly in Serrekunda, Brikama, Bakau, and the rapidly developing Kombo corridor.'
))
story.append(p(
    'However, this economic growth masks significant structural challenges in the labor market. The Gambia '
    'Bureau of Statistics reports that youth unemployment stands at a staggering 41.5% for individuals aged '
    '15-35, with a NEET (Not in Education, Employment, or Training) rate of 41.3%. Perhaps more critically, '
    '81% of all employment in The Gambia is informal, meaning workers lack contracts, social protection, or '
    'access to formal financial services. The construction sector is among the most affected by informality, '
    'with the majority of plumbers, electricians, masons, carpenters, and other tradespeople operating without '
    'formal registration, professional certification, or access to credit and insurance.'
))

story.append(h2('2.2 Skills Gap and Training Challenges'))
story.append(p(
    'Employers across The Gambia consistently report that TVET (Technical and Vocational Education and Training) '
    'graduates lack the practical skills required by industry. Beyond technical competence, employers cite '
    'reliability, work ethic, communication skills, and time management as critical gaps. This creates a '
    'paradox: despite high unemployment, businesses struggle to find dependable skilled workers. GamSkillHub '
    'addresses this gap not only by connecting workers to opportunities, but by creating a merit-based system '
    'where ratings, reviews, and verified credentials incentivize professional development and reliability.'
))
story.append(p(
    'The platform\'s built-in worker verification system, skills assessment, and rating mechanism directly '
    'tackle these quality concerns. By making reliability visible and rewarding it with more job opportunities, '
    'GamSkillHub creates a virtuous cycle where workers invest in their own professional development to improve '
    'their standing on the platform. This market-driven approach to quality improvement is far more sustainable '
    'than traditional training interventions, because it is directly tied to income incentives.'
))

story.append(h2('2.3 Daily Wage Structure for Skilled Trades'))
story.append(p(
    'Understanding the prevailing wage structure is essential for setting competitive pricing on the platform. '
    'The following table summarizes current daily wages for skilled trades in The Gambia, providing a baseline '
    'for pricing and commission calculations:'
))

story.append(Spacer(1, 12))
story.append(make_table(
    ['Trade Category', 'Daily Wage (Dalasi)', 'Monthly Estimate', 'Experience Level'],
    [
        ['Foreman / Supervisor', 'D1,000 - D1,200', 'D20,000 - D24,000', '10+ years'],
        ['Electrician / Solar Tech', 'D750 - D900', 'D15,000 - D18,000', '5-10 years'],
        ['Plumber', 'D700 - D850', 'D14,000 - D17,000', '5-10 years'],
        ['Mason / Bricklayer', 'D750 - D850', 'D15,000 - D17,000', '3-8 years'],
        ['Carpenter / Furniture', 'D700 - D850', 'D14,000 - D17,000', '5-10 years'],
        ['Painter', 'D600 - D750', 'D12,000 - D15,000', '3-7 years'],
        ['Tiler', 'D700 - D800', 'D14,000 - D16,000', '3-8 years'],
        ['Welder / Metal Fabricator', 'D750 - D900', 'D15,000 - D18,000', '5-12 years'],
        ['AC / HVAC Technician', 'D800 - D1,000', 'D16,000 - D20,000', '5-10 years'],
        ['General Labourer', 'D400 - D500', 'D8,000 - D10,000', '1-3 years'],
        ['Home Barber / Cleaner', 'D300 - D600', 'D6,000 - D12,000', '1-5 years'],
    ],
    col_widths=[110, 90, 95, 85]
))
story.append(Paragraph('<i>Table 1: Daily Wage Ranges for Skilled Trades in The Gambia (2025-2026)</i>', caption_style))
story.append(Spacer(1, 12))

story.append(p(
    'These wage levels present a significant opportunity for platform-mediated pricing. By offering transparent, '
    'standardized pricing, GamSkillHub can reduce negotiation friction, eliminate underpricing by workers '
    'unaware of market rates, and provide clients with predictable costs. The platform can set minimum price '
    'floors that protect workers from exploitation while remaining competitive with informal market rates.'
))

# ══════════════════════════════════════════════════════════════
# 3. REAL ESTATE GROWTH & CONSTRUCTION BOOM
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('3. Real Estate Growth and Construction Boom', h1_style))

story.append(h2('3.1 Housing Deficit and Government Response'))
story.append(p(
    'The Gambia faces a severe housing deficit estimated at over 128,000 units, a figure that continues to grow '
    'as the urban population expands at approximately 4% annually. In response, the government announced an '
    'ambitious 200,000-unit affordable housing project in December 2025, representing one of the most significant '
    'public infrastructure commitments in the country\'s history. This project alone will require tens of '
    'thousands of skilled workers across plumbing, electrical, masonry, carpentry, roofing, tiling, and painting '
    'disciplines, creating an unprecedented demand for coordinated labor supply.'
))
story.append(p(
    'For GamSkillHub, this housing initiative represents a transformative opportunity. The platform can serve as '
    'the primary labor procurement channel for both government-contracted developers and private sector builders '
    'working on these housing projects. By aggregating verified, rated workers and providing workforce management '
    'tools, GamSkillHub can position itself as an essential partner in the national housing delivery program. '
    'The platform\'s ability to track worker availability, skills, and performance history makes it ideally '
    'suited to manage the complex logistics of large-scale construction labor deployment.'
))

story.append(h2('3.2 Major Real Estate Developments'))
story.append(p(
    'The Kombo corridor, stretching from Banjul through Serrekunda to Brufut and beyond, has become the '
    'epicenter of real estate development in The Gambia. Several landmark projects are reshaping the landscape '
    'and driving demand for skilled services:'
))

story.append(Spacer(1, 10))
story.append(make_table(
    ['Development', 'Location', 'Investment', 'Key Details'],
    [
        ['Sablux Development', 'Kombo Area', '$200 Million', 'Mixed-use residential and commercial complex'],
        ['Brufut Heights', 'Brufut', '$238K+ per unit', 'Luxury villas with premium finishes'],
        ['Bijilo Apartments', 'Bijilo', '88,750+ Euros', 'Modern residential apartments'],
        ['TUI Blue Tamala Hotel', 'Kotu', 'Undisclosed', 'International hotel, opened Nov 2025'],
        ['Sama 5-Star Hotel', 'Coastal', 'Undisclosed', 'Under construction, premium facility'],
        ['200,000 Housing Units', 'National', 'Government-backed', 'Affordable housing program announced Dec 2025'],
    ],
    col_widths=[95, 70, 80, 150]
))
story.append(Paragraph('<i>Table 2: Major Real Estate Developments Driving Skilled Labor Demand</i>', caption_style))
story.append(Spacer(1, 12))

story.append(p(
    'Foreign direct investment (FDI) flows have consistently exceeded $200 million annually in 2022-2023, '
    'with the government actively encouraging foreign participation in real estate and construction. The OIC '
    'Summit legacy investments include $50 million in new roads, airport modernization, and the completed '
    'Banjul-Serrekunda expressway (May 2024). These infrastructure improvements have opened previously '
    'inaccessible areas for development, further expanding the geographic footprint of construction activity '
    'and the associated demand for skilled tradespeople.'
))

story.append(h2('3.3 Diaspora Investment and Its Impact'))
story.append(p(
    'The Gambian diaspora plays a uniquely important role in the real estate sector. Remittances constitute '
    'a substantial portion of GDP, and a significant share of these funds is directed toward property '
    'construction and renovation. Diaspora investors frequently face challenges in supervising construction '
    'projects remotely, ensuring quality workmanship, and finding reliable tradespeople for ongoing maintenance '
    'of their properties. GamSkillHub directly addresses these pain points by providing a transparent, '
    'review-based platform where diaspora investors can browse verified workers, view portfolios of past work, '
    'read client reviews, and remotely book services for their properties. The platform can also offer project '
    'management features specifically designed for diaspora clients, including photo/video progress updates, '
    'milestone-based payments, and dispute resolution.'
))

# ══════════════════════════════════════════════════════════════
# 4. GOVERNMENT PROCUREMENT & PUBLIC CONTRACTS
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('4. Government Procurement and Public Contracts', h1_style))

story.append(h2('4.1 Public Procurement Framework'))
story.append(p(
    'The Gambia Public Procurement Authority (GPPA) Act of 2022 governs all public procurement processes, '
    'establishing transparent procedures for awarding government contracts. Procurement methods include National '
    'Competitive Bidding (NCB), International Competitive Bidding (ICB), restricted tendering, and single-source '
    'procurement for specialized services. GAMWORKS serves as the key implementing agency for donor-funded '
    'infrastructure projects, including those financed by the World Bank, African Development Bank, and bilateral '
    'donors. There are currently over 291 active government tenders tracked on GlobalTenders, spanning '
    'construction, maintenance, equipment supply, and professional services.'
))

story.append(h2('4.2 World Bank and Donor-Funded Projects'))
story.append(p(
    'A $52.6 million World Bank Gambia Infrastructure Program (GIP) was approved in May 2025, focusing on '
    'transport and energy infrastructure. This program, along with ongoing AFD (French Development Agency) '
    'funded projects, creates sustained demand for skilled construction workers. These donor-funded projects '
    'typically require formal labor management systems, worker verification, safety compliance, and transparent '
    'payment tracking. GamSkillHub\'s platform is architecturally designed to meet these requirements, making '
    'it a compelling partner for organizations implementing donor-funded infrastructure programs in The Gambia.'
))

story.append(h2('4.3 The Government Maintenance Gap'))
story.append(p(
    'One of the most significant opportunities identified in this analysis is the absence of a centralized '
    'maintenance management system for public buildings in The Gambia. Government offices, schools, hospitals, '
    'and public facilities across the country require ongoing maintenance, including plumbing repairs, electrical '
    'work, painting, carpentry, HVAC servicing, and general upkeep. Currently, these maintenance needs are '
    'addressed through ad-hoc arrangements, often resulting in delayed repairs, unreliable workmanship, and '
    'lack of cost control. GamSkillHub can fill this gap by offering government institutions a centralized '
    'digital procurement platform for maintenance services, complete with worker verification, transparent '
    'pricing, quality tracking through ratings and reviews, and digital payment processing for audit compliance.'
))

story.append(callout(
    'Strategic Opportunity: By partnering with GAMWORKS or individual ministries, GamSkillHub can become the '
    'de facto digital procurement platform for government facility maintenance, capturing a significant and '
    'recurring revenue stream from public sector contracts.'
))

# ══════════════════════════════════════════════════════════════
# 5. INDUSTRY CLIENT BASE ANALYSIS
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('5. Industry Client Base Analysis', h1_style))

story.append(h2('5.1 Banking Sector'))
story.append(p(
    'The Gambia\'s banking sector comprises 12-15 commercial banks, including major institutions such as '
    'Access Bank (which acquired Standard Chartered\'s operations), Ecobank, Trust Bank, GTBank, Zenith Bank, '
    'FBN Bank, and Mega Bank. Each of these banks maintains a network of branches and offices across the country '
    'that require ongoing maintenance services including electrical systems, plumbing, HVAC, painting, pest '
    'control, security system installation, and general facility upkeep. Banks also frequently undertake branch '
    'renovations, ATM installation projects, and new branch construction, all of which require skilled tradespeople.'
))
story.append(p(
    '<b>How GamSkillHub Benefits Banks:</b> The platform provides banks with a centralized, transparent '
    'procurement channel for maintenance and renovation services. Instead of relying on informal networks and '
    'individual contractor relationships, banks can use GamSkillHub to post maintenance requests, receive bids '
    'from verified workers, track job progress, and process payments through a single digital platform. This '
    'reduces procurement costs, improves service quality through competition and ratings, and provides a '
    'complete audit trail for compliance purposes. Volume-based B2B pricing can offer banks 10-20% discounts '
    'on platform fees for committing to monthly maintenance contracts.'
))

story.append(h2('5.2 Hotels and Hospitality'))
story.append(p(
    'The tourism and hospitality sector is a cornerstone of the Gambian economy, with hotels ranging from '
    'international chains like TUI Blue Tamala (opened November 2025) and the upcoming Sama 5-star hotel, to '
    'established properties like Kairaba Beach Hotel and Senegambia Hotel, to numerous guesthouses and eco-lodges. '
    'These properties have continuous, high-volume maintenance needs including room maintenance, pool maintenance, '
    'landscaping, plumbing, electrical, HVAC, painting, and pest control. The Middle East and Africa contract '
    'cleaning market alone is projected to add over $10.25 billion by 2026-2031, indicating the massive scale '
    'of opportunity in facility maintenance.'
))
story.append(p(
    '<b>How GamSkillHub Benefits Hotels:</b> Hotels can establish recurring monthly maintenance contracts through '
    'the platform, ensuring a reliable supply of pre-vetted workers for both routine maintenance and emergency '
    'repairs. The platform\'s worker rating system helps hotels identify the most reliable professionals, while '
    'the ability to track worker history and job completion records simplifies quality assurance and reporting '
    'for management. During peak tourist season (November to April), hotels often struggle to find enough '
    'skilled workers; GamSkillHub can solve this seasonal shortage by maintaining an active pool of verified '
    'workers available for on-demand deployment.'
))

story.append(h2('5.3 Telecommunications'))
story.append(p(
    'The telecommunications sector in The Gambia is undergoing significant modernization, with a $50 million '
    'GAMTEL broadband upgrade underway, QCell deploying 5G infrastructure, and Africell expanding its 4G '
    'network. Tower construction, fiber optic installation, office maintenance, and equipment installation all '
    'require specialized skilled workers. The sector is characterized by a mix of permanent technical staff and '
    'outsourced contractors for installation, maintenance, and construction projects. Telecommunications '
    'companies value speed, reliability, and technical competence, all of which GamSkillHub\'s rating and '
    'verification system is designed to surface.'
))
story.append(p(
    '<b>How GamSkillHub Benefits Telecoms:</b> Telecom companies can use the platform to quickly source '
    'specialized technicians for tower maintenance, fiber optic installation, office fit-outs, and equipment '
    'installation across the country. The platform\'s geolocation features allow workers to be matched to '
    'job sites based on proximity, reducing response times for urgent maintenance requests. For large-scale '
    'deployment projects, GamSkillHub can provide workforce management tools including scheduling, progress '
    'tracking, and consolidated billing.'
))

story.append(h2('5.4 Real Estate Developers and Property Managers'))
story.append(p(
    'Property developers and management companies represent perhaps the most natural client segment for '
    'GamSkillHub. Companies managing multiple residential or commercial properties need a reliable pipeline of '
    'skilled workers for unit turnover preparation (painting, cleaning, repairs), ongoing maintenance, and '
    'renovation projects. With the housing deficit driving rapid construction, many developers are also '
    'becoming property managers, creating a dual revenue opportunity for the platform. The Brufut Heights '
    'development alone will house hundreds of families requiring ongoing maintenance services, representing a '
    'significant recurring revenue opportunity.'
))

story.append(Spacer(1, 10))
story.append(make_table(
    ['Industry', 'Key Players', 'Primary Services Needed', 'Revenue Potential'],
    [
        ['Banking', 'Ecobank, Access Bank, Trust Bank, GTBank', 'Branch maintenance, renovations, ATM installation', 'D5-10M/year'],
        ['Hotels / Hospitality', 'TUI Blue, Kairaba, Senegambia', 'Room maintenance, HVAC, plumbing, landscaping', 'D8-15M/year'],
        ['Telecommunications', 'Gamtel, Africell, QCell', 'Tower work, fiber optic, office maintenance', 'D3-7M/year'],
        ['Real Estate Developers', 'Sablux, Brufut Heights, private builders', 'Construction labor, finishing, maintenance', 'D15-30M/year'],
        ['Government Institutions', 'Ministries, schools, hospitals', 'Facility maintenance, renovations, repairs', 'D10-25M/year'],
        ['Property Managers', 'Rental agencies, estate managers', 'Unit preparation, ongoing maintenance', 'D5-12M/year'],
        ['Manufacturing', 'Duraplast, Gambia Brewery, Bell Bottling', 'Equipment maintenance, facility upkeep', 'D2-5M/year'],
        ['Diaspora Investors', 'Individual property owners abroad', 'Construction supervision, property maintenance', 'D5-10M/year'],
    ],
    col_widths=[85, 100, 120, 80]
))
story.append(Paragraph('<i>Table 3: Industry Client Segments and Estimated Revenue Potential</i>', caption_style))
story.append(Spacer(1, 12))

# ══════════════════════════════════════════════════════════════
# 6. HOW GAMSKILLHUB BENEFITS ALL STAKEHOLDERS
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('6. How GamSkillHub Benefits All Stakeholders', h1_style))

story.append(h2('6.1 For Skilled Workers'))
story.append(p(
    'The platform provides skilled workers with access to a steady stream of job opportunities that they would '
    'otherwise find through informal networks, word-of-mouth referrals, or physical presence at gathering spots. '
    'Workers gain a digital identity and professional reputation through verified profiles, ratings, and reviews '
    'that follow them throughout their career. The platform enables workers to command fair market rates through '
    'transparent pricing, reducing the information asymmetry that often leads to underpricing. Perhaps most '
    'importantly, workers who consistently deliver quality work can build a reputation that directly translates '
    'into higher earnings, more job opportunities, and access to premium client segments including hotels, '
    'banks, and government institutions.'
))
story.append(p(
    'Additionally, the escrow-based payment system ensures that workers are guaranteed payment for completed '
    'work, eliminating the common problem of non-payment or delayed payment that plagues informal arrangements. '
    'The platform also opens pathways to formal financial services: workers who earn through GamSkillHub build '
    'a digital transaction history that can be used to access microfinance loans, insurance products, and '
    'mobile banking services from partner financial institutions.'
))

story.append(h2('6.2 For Homeowners and Individual Clients'))
story.append(p(
    'Individual clients gain access to a curated pool of verified, rated professionals with transparent pricing '
    'and quality guarantees. Instead of relying on unreliable recommendations or random encounters with '
    'tradespeople, homeowners can browse worker profiles, read reviews from previous clients, view portfolios '
    'of past work, and make informed hiring decisions. The platform\'s dispute resolution mechanism provides '
    'a safety net that informal arrangements cannot match, while the rating system creates accountability '
    'that incentivizes quality workmanship. For diaspora property owners, the platform offers a particularly '
    'valuable service: the ability to remotely manage maintenance and renovation of their Gambian properties, '
    'with photo/video progress updates and milestone-based payment controls.'
))

story.append(h2('6.3 For Government'))
story.append(p(
    'Government institutions benefit from GamSkillHub as a digital procurement tool that brings transparency, '
    'efficiency, and accountability to facility maintenance spending. The platform provides complete audit '
    'trails for all transactions, worker verification records, quality metrics through ratings, and '
    'standardized pricing that helps prevent overcharging. For ministries managing large portfolios of public '
    'buildings, GamSkillHub offers centralized workforce management that reduces administrative burden, '
    'improves response times for maintenance requests, and generates data on workforce utilization and spending '
    'patterns that can inform budget planning. The platform also supports the government\'s broader objectives '
    'of formalizing the informal economy, creating decent employment opportunities for youth, and promoting '
    'digital transformation in public services.'
))

story.append(h2('6.4 For Corporate Clients'))
story.append(p(
    'Banks, hotels, telecoms, and other corporate clients benefit from reduced procurement costs through '
    'competitive bidding, improved quality through rating-based selection, simplified administration through '
    'centralized billing and reporting, and reduced risk through worker verification and escrow payments. '
    'Corporate accounts with monthly or annual contracts provide predictable costs and priority access to '
    'the platform\'s best-rated workers. Volume-based pricing tiers create additional savings for high-frequency '
    'users, making GamSkillHub a cost-effective alternative to maintaining in-house maintenance teams or '
    'managing multiple individual contractor relationships.'
))

# ══════════════════════════════════════════════════════════════
# 7. CURRENT PLATFORM PAYMENT ANALYSIS
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('7. Current Platform Payment Analysis', h1_style))

story.append(h2('7.1 Existing Payment Flow'))
story.append(p(
    'An analysis of the current GamSkillHub codebase reveals that the payment system is in a prototype phase. '
    'The existing implementation uses a basic browser <b>confirm()</b> dialog that asks clients whether they '
    'wish to pay via "Wave/Bank Transfer" (digital) or "Cash on Delivery" (cash). If the digital option is '
    'selected, a mock alert displays a placeholder message indicating MODEM PAY integration, referencing a '
    'fixed price of D500.00. There is no actual payment gateway connected, no pricing engine, no commission '
    'calculation, and no escrow functionality. The payment_method field is stored with the order in Supabase, '
    'but no further payment processing occurs.'
))
story.append(p(
    'This means the platform currently has no mechanism to collect payment, no way to deduct platform commission, '
    'and no automated payout system for workers. The pricing is hardcoded rather than calculated based on service '
    'type, duration, materials, or market rates. There is no invoice generation, no receipt system, and no '
    'payment history tracking for either clients or workers. While the Supabase database schema includes an '
    'orders table with fields for client details, worker assignment, and status tracking, the financial '
    'components of the transaction lifecycle are entirely unimplemented.'
))

story.append(h2('7.2 Critical Payment Gaps Identified'))

story.append(Spacer(1, 8))
story.append(make_table(
    ['Gap', 'Current State', 'Required Implementation', 'Priority'],
    [
        ['Payment Gateway', 'None (mock confirm dialog)', 'Integrate Wave API, Modem Pay, or PawaPay', 'Critical'],
        ['Pricing Engine', 'Hardcoded D500.00', 'Dynamic pricing by service type, duration, materials', 'Critical'],
        ['Commission System', 'Not implemented', 'Calculate and deduct 10-20% platform commission', 'Critical'],
        ['Escrow System', 'Not implemented', 'Hold client payment until job completion confirmed', 'High'],
        ['Worker Payouts', 'Not implemented', 'Automated payouts via Wave/mobile money', 'High'],
        ['Invoice Generation', 'Not implemented', 'Auto-generate invoices with tax breakdown', 'Medium'],
        ['Receipt System', 'Not implemented', 'SMS/email receipts after payment', 'Medium'],
        ['Payment History', 'Not implemented', 'Full transaction history for clients and workers', 'Medium'],
        ['Corporate Billing', 'Not implemented', 'Monthly consolidated invoices for B2B clients', 'High'],
        ['Refund/Dispute', 'Not implemented', 'Automated dispute resolution and refund workflow', 'High'],
    ],
    col_widths=[90, 100, 140, 55]
))
story.append(Paragraph('<i>Table 4: Payment System Gap Analysis and Implementation Priorities</i>', caption_style))
story.append(Spacer(1, 12))

story.append(h2('7.3 Who Should Pay?'))
story.append(p(
    'The payment model should be designed around the principle that <b>the client pays for services received, '
    'and the platform earns commission from each transaction</b>. This is the standard model used by all '
    'successful service marketplaces globally, including SweepSouth (20% commission), Lynk (commission-based), '
    'and ride-hailing platforms (15-25% commission). The specific structure should work as follows:'
))
story.append(bullet(
    '<b>Client pays the full service fee</b> at the time of booking or upon job completion, depending on the '
    'service type. For small jobs (under D2,000), payment at booking via the platform ensures worker '
    'commitment. For larger projects, milestone-based payments provide protection for both parties.'
))
story.append(bullet(
    '<b>Platform deducts a commission</b> of 10-15% from each transaction. This commission covers platform '
    'maintenance, payment processing costs, marketing, customer support, and profit margin. The commission '
    'rate can be tiered based on transaction value or subscription level.'
))
story.append(bullet(
    '<b>Worker receives the net amount</b> (85-90% of the service fee) directly to their mobile money wallet '
    'or bank account. Payouts can be instant (with a small fee) or scheduled (free, weekly or bi-weekly).'
))
story.append(bullet(
    '<b>No registration fees for workers</b> initially. The platform should be free to join to maximize worker '
    'supply. Once a critical mass is achieved, optional premium subscriptions (D500-1,500/month) can be '
    'introduced for enhanced visibility and priority access to leads.'
))

# ══════════════════════════════════════════════════════════════
# 8. PAYMENT INTEGRATION STRATEGY
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('8. Payment Integration Strategy', h1_style))

story.append(h2('8.1 Payment Landscape in The Gambia'))
story.append(p(
    'The Gambian payment ecosystem is undergoing rapid transformation, driven by mobile money adoption, '
    'regulatory modernization, and the emergence of local payment aggregators. The Central Bank of Gambia '
    'has been actively developing the regulatory framework for digital payments, publishing the Payment '
    'Systems Regulation in 2019 and advancing a Fintech Policy Zero Draft in 2024. The landmark launch '
    'of BANTABA 2.0 in December 2025, built on the Mojaloop open-source real-time payment switch, connects '
    'banks and mobile wallets for the first time, enabling instant interoperable payments across the entire '
    'financial system. The NPSAC (National Payment Switch and Central Infrastructure) governance committee '
    'was launched in February 2026 to oversee this infrastructure.'
))

story.append(h2('8.2 Mobile Money Providers'))

story.append(Spacer(1, 8))
story.append(make_table(
    ['Provider', 'Users', 'Key Strengths', 'API Available'],
    [
        ['Wave', '10M+ (regional)', 'Zero-fee merchant Scan & Pay, lowest cost transfers (1%)', 'Yes - Business API'],
        ['QMoney / Qodoo', 'Highest adoption (69%)', 'Dominant local user base, CBG-licensed', 'Limited'],
        ['Afrimoney (Africell)', '1.5M+ users', 'Integrated with Africell mobile network', 'Yes'],
        ['Orange Money', 'Growing', 'Cross-border capability, pan-African reach', 'Yes'],
        ['eMoney', 'Active', 'CBG-licensed, government partnerships', 'Limited'],
    ],
    col_widths=[85, 90, 150, 80]
))
story.append(Paragraph('<i>Table 5: Mobile Money Providers in The Gambia</i>', caption_style))
story.append(Spacer(1, 12))

story.append(h2('8.3 Payment Aggregators'))
story.append(p(
    '<b>Modem Pay</b> is the premier local payment gateway in The Gambia, offering developer-friendly REST APIs '
    'that support all mobile money providers, card payments, and bank transfers. It is the most practical first '
    'integration target for GamSkillHub because of its local presence, comprehensive coverage of Gambian payment '
    'methods, and established track record with Gambian businesses including GamShows for online ticketing.'
))
story.append(p(
    '<b>PawaPay</b> offers a pan-African mobile money aggregation API covering 20+ markets including The Gambia, '
    'with 218 million+ accessible customers. It supports collections, refunds, disbursements, and batch '
    'disbursements through a single API. PawaPay is ideal as a secondary or scaling integration, particularly '
    'if GamSkillHub plans to expand beyond The Gambia to Senegal, Guinea-Bissau, or other West African markets.'
))
story.append(p(
    '<b>Wave Business API</b> provides direct integration with Wave\'s merchant services, including Checkout '
    '(initiate payments), Payout (send money to Wave users), Balance (check merchant balance), and Merchant '
    'APIs. With Wave\'s dominant market position and zero-fee merchant payments, integrating the Wave Business '
    'API is essential for maximizing payment adoption among Gambian clients and workers.'
))

story.append(h2('8.4 Recommended Payment Architecture'))
story.append(p(
    'The recommended payment architecture follows a three-tier approach that prioritizes reliability, '
    'coverage, and cost-effectiveness:'
))
story.append(bullet(
    '<b>Tier 1 - Primary (Launch): Modem Pay</b> - Integrate Modem Pay as the primary payment gateway '
    'for its comprehensive coverage of all Gambian payment methods, local support, and proven reliability. '
    'This handles Wave, QMoney, Afrimoney, Orange Money, eMoney, card payments, and bank transfers through '
    'a single integration.'
))
story.append(bullet(
    '<b>Tier 2 - Direct: Wave Business API</b> - Add direct Wave integration for Wave-specific optimizations '
    'including Scan & Pay (QR code payments), instant payouts to workers, and zero-fee merchant collections. '
    'Wave should be promoted as the preferred payment method due to its market dominance and low cost.'
))
story.append(bullet(
    '<b>Tier 3 - Scaling: PawaPay</b> - Integrate PawaPay as a backup and for batch disbursements (paying '
    'multiple workers simultaneously), reducing per-transaction costs for large-scale payout operations. '
    'PawaPay also provides a pathway for regional expansion.'
))

story.append(h2('8.5 Escrow Payment Implementation'))
story.append(p(
    'The escrow system is central to building trust on the platform. The recommended implementation follows '
    'this workflow: (1) The client pays the full service fee when placing an order; (2) Funds are held in '
    'a secure escrow account managed by the payment gateway; (3) When the worker completes the job and the '
    'client confirms satisfaction (or the auto-completion timer expires after 24-48 hours), the funds are '
    'released; (4) The platform automatically deducts its commission and disburses the net amount to the '
    'worker\'s mobile money wallet or bank account; (5) If a dispute arises before confirmation, funds remain '
    'in escrow until resolution through the platform\'s dispute resolution process. This model protects both '
    'parties: clients know their money is safe until the job is done, and workers know they will be paid upon '
    'completion. Flutterwave\'s Escrow Payments API provides a proven reference implementation for this pattern.'
))

# ══════════════════════════════════════════════════════════════
# 9. MONETIZATION STRATEGIES
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('9. Monetization Strategies', h1_style))

story.append(h2('9.1 Commission-Based Revenue (Primary)'))
story.append(p(
    'The primary revenue model is a commission on each transaction processed through the platform. Based on '
    'analysis of comparable African service platforms, the recommended commission structure is as follows:'
))

story.append(Spacer(1, 8))
story.append(make_table(
    ['Revenue Stream', 'Rate / Amount', 'Frequency', 'Target Segment'],
    [
        ['Service Commission', '15% of transaction value', 'Per booking', 'All clients'],
        ['B2B Subscription (Basic)', 'D5,000/month', 'Monthly', 'Small businesses'],
        ['B2B Subscription (Pro)', 'D15,000/month', 'Monthly', 'Hotels, banks, government'],
        ['B2B Subscription (Enterprise)', 'D50,000/month', 'Monthly', 'Large developers, ministries'],
        ['Worker Premium Plan', 'D750/month', 'Monthly', 'Individual workers'],
        ['Featured Listing', 'D200/day', 'Per day', 'Workers seeking visibility'],
        ['Lead Generation Fee', 'D50-100 per lead', 'Per lead', 'Workers in high-value trades'],
        ['Advertising', 'D5,000-20,000/month', 'Monthly', 'Hardware stores, suppliers'],
        ['Training / Certification', 'D1,000-3,000 per course', 'Per course', 'Workers upgrading skills'],
        ['Data / Market Intelligence', 'Custom pricing', 'Quarterly', 'Government, NGOs, researchers'],
    ],
    col_widths=[100, 95, 70, 120]
))
story.append(Paragraph('<i>Table 6: Comprehensive Revenue Streams for GamSkillHub</i>', caption_style))
story.append(Spacer(1, 12))

story.append(p(
    'The 15% commission rate positions GamSkillHub competitively within the African service marketplace range '
    'of 15-25% (SweepSouth charges 20%, ride-hailing platforms charge 15-25%). This rate balances revenue '
    'generation with worker affordability, ensuring that the platform remains attractive to both sides of the '
    'market. For context, a typical plumbing job valued at D2,500 would generate D375 in platform commission, '
    'while a larger electrical installation job valued at D15,000 would generate D2,250.'
))

story.append(h2('9.2 B2B Subscription Model'))
story.append(p(
    'Corporate clients present the highest-value revenue opportunity through subscription plans that provide '
    'priority access, dedicated account management, and reduced commission rates. The tiered structure '
    'accommodates businesses of all sizes, from small guesthouses to government ministries. Each tier '
    'includes a defined number of job postings per month, priority worker matching, consolidated monthly '
    'billing, and service level agreements (SLAs) guaranteeing response times. The Enterprise tier adds '
    'custom API integration, dedicated workforce allocation, and executive-level reporting with workforce '
    'utilization analytics and spending forecasts.'
))
story.append(p(
    'To illustrate the revenue potential: if GamSkillHub signs just 5 bank branches at the Basic tier '
    '(D5,000/month each), 3 hotels at the Pro tier (D15,000/month each), and 1 government ministry at '
    'the Enterprise tier (D50,000/month), the monthly subscription revenue alone would be D120,000 '
    '(approximately D1.44 million annually), excluding commission income from jobs booked through these accounts.'
))

story.append(h2('9.3 Worker Premium Plans'))
story.append(p(
    'While registration should remain free to maximize worker supply, premium plans offer enhanced visibility '
    'and features for workers who want to grow their business on the platform. The Premium Plan (D750/month) '
    'includes a "Verified Pro" badge displayed on their profile, priority placement in search results, access '
    'to premium job leads from corporate clients, and a dedicated profile page with portfolio showcase. '
    'Workers can also pay per-lead fees (D50-100) as an alternative to monthly subscriptions, paying only '
    'when they receive qualified job leads. This pay-per-lead model is particularly effective for high-value '
    'trades like solar installation, where a single job can pay D10,000-50,000.'
))

story.append(h2('9.4 Revenue Projections (3-Year)'))
story.append(Spacer(1, 8))
story.append(make_table(
    ['Revenue Stream', 'Year 1', 'Year 2', 'Year 3'],
    [
        ['Transaction Commission', 'D2.4M', 'D8.5M', 'D22M'],
        ['B2B Subscriptions', 'D600K', 'D2.4M', 'D6M'],
        ['Worker Premium Plans', 'D180K', 'D720K', 'D1.8M'],
        ['Advertising Revenue', 'D120K', 'D480K', 'D1.2M'],
        ['Training/Certification', 'D60K', 'D360K', 'D1.2M'],
        ['Data/Market Intelligence', 'D0', 'D120K', 'D600K'],
        ['Total Revenue', 'D3.36M', 'D12.58M', 'D32.8M'],
    ],
    col_widths=[120, 85, 85, 85]
))
story.append(Paragraph('<i>Table 7: Three-Year Revenue Projections (Estimated, in Dalasi)</i>', caption_style))
story.append(Spacer(1, 12))

story.append(callout(
    'At projected Year 3 revenue of D32.8 million (approximately $460,000), GamSkillHub would be among the '
    'most successful tech startups in The Gambia. These projections assume 500 workers and 2,000 transactions '
    'in Year 1, growing to 3,000 workers and 15,000 transactions by Year 3.'
))

# ══════════════════════════════════════════════════════════════
# 10. GO-TO-MARKET PLAN
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('10. Go-To-Market Plan', h1_style))

story.append(h2('10.1 Where Do We Start?'))
story.append(p(
    'The go-to-market strategy should be geographically focused initially, starting in the <b>Greater Banjul '
    'Area (GBA)</b>, specifically Serrekunda, Bakau, Kotu, Fajara, and Kololi. This region has the highest '
    'concentration of potential clients (homeowners, businesses, hotels) and skilled workers. It also has the '
    'best internet connectivity, highest smartphone penetration, and most developed mobile money infrastructure. '
    'Starting in a concentrated geographic area allows the platform to build density, ensuring that clients '
    'who post jobs receive quick responses from nearby workers, which is essential for building trust and '
    'demonstrating value before expanding to Brikama, Latrikunda, and eventually the rest of the country.'
))

story.append(h2('10.2 When Do We Start?'))
story.append(p(
    'The recommended timeline follows a phased approach that prioritizes getting the core product right before '
    'scaling. Phase 1 (Months 1-3) focuses on completing payment integration (Modem Pay + Wave), implementing '
    'the commission engine, and conducting beta testing with 50 workers and 200 clients in Serrekunda. '
    'Phase 2 (Months 4-6) involves the public launch across the Greater Banjul Area, targeting 500 workers '
    'and 2,000 clients, with active marketing through social media, community events, and partnership outreach. '
    'Phase 3 (Months 7-12) focuses on B2B client acquisition, signing the first corporate accounts (hotels, '
    'banks), and launching worker premium plans. Phase 4 (Year 2) extends coverage to Brikama, Latrikunda, '
    'Sukuta, and begins regional expansion planning.'
))

story.append(h2('10.3 Who Do We Start With?'))
story.append(p(
    '<b>Worker Acquisition (First 500):</b> The initial cohort of workers should be concentrated in the '
    'highest-demand trades: plumbing, electrical, masonry, carpentry, and painting. These are the trades '
    'with the most consistent demand from both individual homeowners and corporate clients. Workers should be '
    'recruited through artisan association partnerships, physical onboarding events at worker gathering points, '
    'WhatsApp group outreach, and community leader referrals. Each worker should undergo basic verification '
    '(ID check, skills assessment) before being listed on the platform. The first 100 workers should be '
    'personally vetted by the founding team to ensure quality standards are established from day one.'
))
story.append(p(
    '<b>Client Acquisition (First 2,000):</b> The initial client base should target urban middle-class '
    'homeowners (ages 25-45) in the Serrekunda-Bakau-Kotu corridor, who are the most likely to adopt a '
    'digital platform for hiring skilled workers. Marketing channels should include Facebook and Instagram '
    'advertising (most popular social platforms in Gambia), WhatsApp community groups, radio advertisements '
    'on local stations, and physical flyers at estate agent offices and building material suppliers. '
    'Simultaneously, the team should begin outreach to 10-15 B2B prospects including 3-5 hotels, 3-4 bank '
    'branches, and 2-3 property management companies, aiming to convert at least 3-5 to paid subscriptions '
    'within the first six months.'
))

story.append(h2('10.4 How Do We Execute?'))
story.append(p(
    '<b>Community-Led Growth:</b> The most effective growth strategy in The Gambia is community-based. '
    'GamSkillHub should recruit "Community Champions" in each target neighborhood, respected individuals '
    'who can vouch for the platform and refer both workers and clients. These champions can be compensated '
    'through a referral program: D200 for each verified worker they refer who completes their first job, and '
    'D100 for each new client who places their first booking. Mosque and church communities, market '
    'associations, and youth groups provide natural networks for this kind of organic, trust-based growth.'
))
story.append(p(
    '<b>Partnership-First Approach:</b> Rather than spending heavily on advertising, GamSkillHub should '
    'prioritize strategic partnerships that provide access to existing client bases. Partnership targets '
    'include: real estate agents (who can recommend GamSkillHub to new homeowners), hardware stores (who can '
    'promote the platform to contractors buying materials), banks (who can offer GamSkillHub as a value-added '
    'service to mortgage customers), and TVET institutions (who can direct graduates to register on the '
    'platform). Each partnership should include a mutual benefit, whether it is referral fees, co-marketing '
    'agreements, or bundled service offerings.'
))

# ══════════════════════════════════════════════════════════════
# 11. PARTNERSHIP & INTEGRATION ROADMAP
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('11. Partnership and Integration Roadmap', h1_style))

story.append(h2('11.1 Wave Integration'))
story.append(p(
    'Wave is the dominant mobile money platform in The Gambia and Senegal, with over 10 million regional '
    'users and the lowest transfer costs in the market (1% per transaction). Integration with Wave should '
    'be implemented at two levels: first, as a payment method via Modem Pay (Tier 1, immediate), and second, '
    'as a direct business partner using the Wave Business API for optimized checkout, Scan and Pay QR codes, '
    'and instant worker payouts. GamSkillHub should negotiate a partnership with Wave that includes preferential '
    'transaction rates for high-volume platform payments, co-marketing opportunities, and access to Wave\'s '
    'merchant analytics tools. In the long term, GamSkillHub workers could receive Wave-branded identification '
    'and be listed in Wave\'s merchant directory, further driving adoption.'
))

story.append(h2('11.2 Bank Integration'))
story.append(p(
    'Partnerships with commercial banks can serve multiple strategic purposes. First, bank integration enables '
    'payment processing for clients who prefer card payments or bank transfers over mobile money. Second, '
    'banks can offer microfinance products to GamSkillHub workers, using their platform transaction history '
    'as collateral assessment data. Third, banks are themselves major clients for facility maintenance services. '
    'The recommended approach is to partner with 2-3 banks initially (Ecobank for its pan-African reach, '
    'Trust Bank for its strong local presence, and Access Bank for its digital innovation focus). Through the '
    'BANTABA 2.0 interoperable payment switch, integration with any bank automatically enables connectivity '
    'to all other banks and mobile wallets on the switch, dramatically reducing integration complexity.'
))

story.append(h2('11.3 Gamride Collaboration'))
story.append(p(
    'Gamride, The Gambia\'s first ride-hailing platform launched in May 2025 on the MWM white-label platform, '
    'offers compelling partnership opportunities. Both platforms serve the Gambian market, and collaboration '
    'could take several forms: (1) Cross-promotion, where GamSkillHub is promoted to Gamride users (and vice '
    'versa), leveraging each other\'s user base; (2) Transport integration, where Gamride provides transportation '
    'for GamSkillHub workers to job sites, particularly in areas with limited public transport; (3) Super-app '
    'evolution, where both platforms eventually merge into a comprehensive services marketplace offering rides, '
    'skilled services, food delivery, and more, following the OPay model in Nigeria. The fare negotiation model '
    'that makes Gamride unique could also be adapted for GamSkillHub\'s pricing system, allowing clients and '
    'workers to negotiate service rates within platform-defined minimum and maximum bounds.'
))

story.append(h2('11.4 Delivery and Logistics Partners'))
story.append(p(
    'As GamSkillHub expands its service offerings to include delivery of materials, tools, and supplies, '
    'partnerships with logistics companies become essential. <b>1Bena</b>, The Gambia\'s only super app '
    '(offering food delivery, rides, and shopping), could serve as a delivery partner for materials procurement. '
    '<b>Indil</b>, the first full-tech delivery app in Gambia with food, product, and courier services, '
    'offers another partnership opportunity, particularly for diaspora-focused property management services '
    'where documents, keys, or materials need to be physically transported. These partnerships can be structured '
    'as API integrations, where GamSkillHub\'s platform triggers delivery orders through partner APIs when a '
    'client purchases materials through the platform.'
))

story.append(h2('11.5 Government and TVET Partnerships'))
story.append(p(
    'Partnerships with government agencies and Technical and Vocational Education and Training (TVET) '
    'institutions can create a sustainable pipeline of verified, trained workers. GAMWORKS, as the key '
    'implementing agency for donor-funded infrastructure, is a natural partner for workforce supply on '
    'large-scale projects. TVET institutions can direct graduates to register on GamSkillHub, creating a '
    'pathway from training to employment. The platform can also partner with the National Youth Service Scheme '
    'and the Ministry of Youth and Sports to provide digital skills training and employment opportunities for '
    'young tradespeople, aligning with the government\'s youth empowerment agenda.'
))

story.append(h2('11.6 Integration Architecture Overview'))

story.append(Spacer(1, 8))
story.append(make_table(
    ['Partner', 'Integration Type', 'What We Integrate', 'Timeline'],
    [
        ['Modem Pay', 'Payment Gateway API', 'All payment methods, cards, bank transfers', 'Month 1-2'],
        ['Wave', 'Business API + Partner', 'Checkout, Scan & Pay, instant payouts', 'Month 2-3'],
        ['PawaPay', 'Aggregation API', 'Batch disbursements, cross-border payments', 'Month 4-6'],
        ['BANTABA 2.0', 'Payment Switch', 'Interoperable bank-to-wallet transfers', 'Month 6-9'],
        ['Gamride', 'Cross-promotion + API', 'Transport for workers, super-app features', 'Month 6-12'],
        ['1Bena / Indil', 'Delivery API', 'Material delivery, document transport', 'Month 9-12'],
        ['Ecobank / Trust Bank', 'Banking API', 'Card payments, microfinance for workers', 'Month 3-6'],
        ['GAMWORKS', 'B2B Partnership', 'Workforce supply for donor-funded projects', 'Month 6-9'],
        ['TVET Institutions', 'Data Feed + Referral', 'Graduate pipeline, training programs', 'Month 4-6'],
    ],
    col_widths=[80, 85, 145, 70]
))
story.append(Paragraph('<i>Table 8: Partnership and Integration Timeline</i>', caption_style))
story.append(Spacer(1, 12))

# ══════════════════════════════════════════════════════════════
# 12. IMPLEMENTATION TIMELINE
# ══════════════════════════════════════════════════════════════
story.extend(add_major_section('12. Implementation Timeline', h1_style))

story.append(h2('12.1 Phase 1: Foundation (Months 1-3)'))
story.append(bullet(
    '<b>Payment Integration:</b> Complete Modem Pay integration (primary gateway), implement Wave Business API '
    'for direct mobile money payments and payouts. Build escrow system, commission engine, and invoice generation.'
))
story.append(bullet(
    '<b>Pricing Engine:</b> Develop dynamic pricing algorithm based on service type, materials, duration, and '
    'location. Implement tiered commission structure (15% standard, reduced rates for B2B subscriptions).'
))
story.append(bullet(
    '<b>Worker Onboarding:</b> Recruit and verify first 200 workers in Serrekunda and Bakau. Conduct in-person '
    'skills assessment for the first 50 to establish quality benchmarks. Set up worker profiles with photos, '
    'skills, and work history portfolios.'
))
story.append(bullet(
    '<b>Beta Testing:</b> Launch closed beta with 200 workers and 100 clients. Collect feedback, fix bugs, '
    'iterate on user experience. Test full payment flow end-to-end including escrow, commission deduction, '
    'and worker payout.'
))

story.append(h2('12.2 Phase 2: Public Launch (Months 4-6)'))
story.append(bullet(
    '<b>Public Launch:</b> Open platform to all users in the Greater Banjul Area. Target 500 workers and '
    '2,000 active clients by end of Month 6. Launch marketing campaign across Facebook, Instagram, radio, '
    'and community events.'
))
story.append(bullet(
    '<b>B2B Outreach:</b> Begin active sales outreach to hotels, banks, and property managers. Aim to sign '
    '3-5 corporate accounts within the first quarter after launch. Develop B2B subscription tiers and '
    'corporate dashboard features.'
))
story.append(bullet(
    '<b>Community Expansion:</b> Deploy Community Champion referral program in target neighborhoods. Partner '
    'with 3-5 artisan associations for worker recruitment. Begin worker registration drives in Brikama and '
    'Latrikunda.'
))

story.append(h2('12.3 Phase 3: Growth (Months 7-12)'))
story.append(bullet(
    '<b>Premium Features:</b> Launch worker premium plans and featured listings. Introduce lead generation '
    'fees for high-value trades. Begin advertising revenue from hardware stores and material suppliers.'
))
story.append(bullet(
    '<b>Geographic Expansion:</b> Extend full coverage to Brikama, Sukuta, Latrikunda, and coastal areas. '
    'Begin planning for regional expansion to Farafenni, Basse, and potential cross-border expansion to '
    'Senegal (Ziguinchor, Dakar).'
))
story.append(bullet(
    '<b>Strategic Partnerships:</b> Formalize partnerships with Wave, banks, GAMWORKS, and TVET institutions. '
    'Begin Gamride integration planning. Launch diaspora-focused property management features.'
))
story.append(bullet(
    '<b>Data Analytics:</b> Build market intelligence dashboard providing insights on pricing trends, demand '
    'patterns, skills gaps, and workforce utilization. Begin packaging anonymized data as a revenue product '
    'for government and institutional clients.'
))

story.append(h2('12.4 Phase 4: Scale (Year 2-3)'))
story.append(bullet(
    '<b>National Coverage:</b> Achieve coverage across all major population centers in The Gambia. Target '
    '3,000+ active workers and 10,000+ active clients by end of Year 2.'
))
story.append(bullet(
    '<b>Government Contracts:</b> Bid on government facility maintenance tenders through GPPA. Position '
    'GamSkillHub as the official digital procurement platform for government maintenance services.'
))
story.append(bullet(
    '<b>Super-App Evolution:</b> Integrate additional services (material marketplace, tool rental, training '
    'courses) to increase user engagement and revenue per user. Explore Gamride and 1Bena integration for '
    'transport and delivery capabilities.'
))
story.append(bullet(
    '<b>Regional Expansion:</b> Leverage PawaPay\'s pan-African coverage to expand into Senegal, '
    'Guinea-Bissau, and potentially Sierra Leone. Adapt the platform for each market\'s local payment '
    'methods, regulatory requirements, and cultural context.'
))

story.append(Spacer(1, 18))
story.append(make_table(
    ['Milestone', 'Target Date', 'Key Metrics', 'Investment Required'],
    [
        ['Payment Integration Complete', 'Month 2', 'Gateway live, escrow working', 'D200,000'],
        ['Beta Launch', 'Month 3', '200 workers, 100 clients, 50 jobs', 'D300,000'],
        ['Public Launch', 'Month 4', 'Platform open, marketing live', 'D500,000'],
        ['First B2B Client', 'Month 6', '5 corporate subscriptions', 'D150,000'],
        ['500 Workers / 2,000 Clients', 'Month 6', 'Revenue: D500K+/month', '-'],
        ['Break-Even Point', 'Month 12', 'Monthly costs covered by revenue', '-'],
        ['1,500 Workers / 5,000 Clients', 'End Year 1', 'Revenue: D3.36M', 'D1M'],
        ['3,000 Workers / 15,000 Clients', 'End Year 2', 'Revenue: D12.58M', 'D2.5M'],
        ['Regional Expansion', 'Year 3', 'Revenue: D32.8M, 2+ countries', 'D5M'],
    ],
    col_widths=[115, 70, 135, 80]
))
story.append(Paragraph('<i>Table 9: Key Milestones and Investment Requirements</i>', caption_style))
story.append(Spacer(1, 12))

story.append(callout(
    'Total estimated investment to reach break-even (Month 12): approximately D1.15 million. This covers '
    'payment integration, marketing, team salaries, and operational costs. Revenue projections suggest '
    'break-even is achievable within 10-12 months with disciplined execution and focused geographic strategy.'
))

# ══════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════
doc.multiBuild(story, onLaterPages=add_page_number, onFirstPage=add_page_number)
print(f"Report generated: {output_path}")
