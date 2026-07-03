from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import utils
import datetime
import os
import numpy as np

#loggin
from Logger import debug, error, info

def format_val(v):
    if isinstance(v, (int, float, np.number)):
        return f"{v:.4f}"
    return str(v)

def generateGlobalPDF(cwd, report_filename, comparison_status, TEST_VERSION, BASE_VERSION):
    debug(f"cwd : {cwd}  report_filename : {report_filename}  comparison_status : {comparison_status} TEST_VERSION : {TEST_VERSION} BASE_VERSION : {BASE_VERSION}")
    doc = SimpleDocTemplate(report_filename, pagesize=letter)
    def shorten_filename(filename):
        if len(filename)>30:
            filename = filename[:30] + "...xlsx"
        return filename

    def version_filename(filename):
        file_name = filename.split('_')
        version = file_name[-1][ :-5]
        return version

    def IPSA_analysis(filename):
        #name_analysisType_version
        file_name = filename.split('_')

        IPSA_file_name = '_'.join(file_name[ :-2])
        analysis = file_name[-2]
        if 'Fault' in analysis:
            analysis = f'Fault Analysis - {" ".join(analysis.split()[-3: ])}'
        if analysis == 'Imp' or analysis == 'Pen' or  analysis == 'Vol':
            mapping = {"Imp": "Impedance Scan", "Pen": "Penetration", "Vol": "Voltage Waveform"}
            analysis = f'Harmonic Analysis - {mapping[analysis]}' if analysis in mapping else analysis

        if len(file_name) > 3:
            component = file_name[2]
        else:
            component = ''
        return IPSA_file_name, analysis, component
        
    def defineTable(data, col_widths, row_heights, alignment, table_style):
        table = Table(data, colWidths=col_widths, rowHeights=row_heights, hAlign=alignment)
        table.wrap(0, 0)
        table.setStyle(table_style)
        return table

    # Function to add company logo and date to header
    def header(canvas, doc):
        canvas.saveState()
        # Add company logo
        image_path = os.path.join(cwd, "images", "ipsalogo.jpg")
        image_reader = utils.ImageReader(image_path)
        canvas.drawImage(image_reader, 40, 725, width=1.5*inch, height=0.7*inch)
        execution_date = datetime.datetime.now().strftime("Date: %B %d, %Y")  # Get current date and format it
        canvas.setFont("Helvetica", 10)
        canvas.drawRightString(550, 750, execution_date)
        canvas.restoreState()

    # Adding header to the document
    doc.build([Paragraph(" ", getSampleStyleSheet()["Normal"])], onFirstPage=header, onLaterPages=header)

    # Add Styles
    heading_style = ParagraphStyle(name='Heading', fontSize=16, textColor=colors.black, 
                                    leading=22, spaceAfter=12, alignment=TA_CENTER, 
                                    fontName='Helvetica-Bold')
    
    paragraph_style = ParagraphStyle(name='Paragraph', fontSize=10, textColor=colors.black, 
                                      leading=16, spaceBefore=0.2*inch, 
                                      fontName='Helvetica-Bold', leftIndent=0.25*inch)
    bullet_stylelarge = ParagraphStyle(name='Bullet', fontSize=11, textColor=colors.black, leading=16, spaceBefore=0.2*inch,spaceAfter=0,fontName='Helvetica-Oblique', 
                                  bulletIndent=0.25*inch, leftIndent=0.25*inch, bulletColor=colors.black)
    
    bullet_style_small = ParagraphStyle(name='Bullet', fontSize=10, textColor=colors.black, leading=16, spaceBefore=0.05*inch,fontName='Helvetica-Oblique', 
                                  bulletIndent=0.25*inch, leftIndent=0.35*inch, bulletColor=colors.black)
    
    #PDF Starts
    elements = [Paragraph("COMPARISON REPORT", heading_style)]
    if comparison_status:
        for file_names, status in comparison_status.items():
            IPSA_test_file_name, analysis, component = IPSA_analysis(file_names[1])
            input_file_name=shorten_filename(IPSA_test_file_name)
            base_file_version=version_filename(file_names[0])
            test_file_version=version_filename(file_names[1])

            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (-1, 0),(0,0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (0,-1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ])
            data = [
                    ['File Name',input_file_name],
                    ['Analysis Type', f'{analysis}'],
                   ]
            if component != '':
                data.append(['Result Type', f'{component}'])
                table_style.add('TEXTCOLOR', (1,5), (1,5), colors.darkred)
            else:
                table_style.add('TEXTCOLOR', (1,4), (1,4), colors.darkred)

            data.extend([
                        ['Base Version',base_file_version ],
                        ['Test Version', test_file_version],
                        ['Comparison Status', 'FAILED']
                       ])

            table = defineTable(data, [175, 250], 25, 'CENTER', table_style)
            elements.append(table)

            elements.append(Paragraph('Highest Differences', bullet_stylelarge))
            # {'Busbars': [{'Load power factor': [0.948683, 5.0, '-81.026%']}]}
            # for sheet_name, data in status[1].items():
            #     elements.append(Paragraph(f'{sheet_name} : {differences}', bullet_style_small))

            for sheet_name, data in status[1].items():
                text = "<br/>".join(f"{col} : Main = {format_val(vals[1])}, Test = {format_val(vals[0])}, Diff = {vals[2]}" for item in data for col, vals in item.items())
                # text = "<br/>".join(f"{col} : Main = {vals[0]:.4f}, Test = {vals[1]:.4f}, Diff = {vals[2]}" for item in data for col, vals in item.items())
                elements.append(Paragraph(f"{sheet_name} :<br/>{text}", bullet_style_small)) 
            elements.append(Paragraph(f"The file can be accessed here: {file_names[2]}", bullet_style_small))
            elements.append(Spacer(1, 50))
    else:
        elements.append(Paragraph(f"There are no differences between the Test[{TEST_VERSION}] and Base[{BASE_VERSION}] versions for all analysis", paragraph_style))

    # Generating PDF
    doc.build(elements)
    info(f"Comparison report generated at {report_filename}")
