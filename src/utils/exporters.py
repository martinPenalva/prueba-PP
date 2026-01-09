"""
Utilidades para exportar datos a CSV y PDF
"""

import csv
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from tkinter import filedialog

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config.config import EXPORT_CONFIG


class CSVExporter:
    """Clase para exportar datos a CSV"""
    
    @staticmethod
    def export_events(events: List[Dict], filepath: Optional[str] = None) -> Optional[str]:
        """Exporta eventos a CSV. Si no se proporciona filepath, usa diálogo de guardado"""
        if filepath is None:
            # Usar diálogo de guardado
            default_filename = f"eventos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
                initialfile=default_filename,
                title="Guardar eventos como CSV"
            )
            
            if not filepath:  # Usuario canceló
                return None
        
        try:
            with open(filepath, 'w', newline='', encoding=EXPORT_CONFIG['csv_encoding']) as f:
                if not events:
                    return filepath
                
                fieldnames = events[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(events)
            
            return filepath
        except Exception as e:
            print(f"Error al exportar CSV: {e}")
            return None
    
    @staticmethod
    def export_participants(participants: List[Dict], filepath: Optional[str] = None) -> Optional[str]:
        """Exporta participantes a CSV. Si no se proporciona filepath, usa diálogo de guardado"""
        if filepath is None:
            # Usar diálogo de guardado
            default_filename = f"participantes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
                initialfile=default_filename,
                title="Guardar participantes como CSV"
            )
            
            if not filepath:  # Usuario canceló
                return None
        
        try:
            with open(filepath, 'w', newline='', encoding=EXPORT_CONFIG['csv_encoding']) as f:
                if not participants:
                    return filepath
                
                fieldnames = participants[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(participants)
            
            return filepath
        except Exception as e:
            print(f"Error al exportar CSV: {e}")
            return None


class PDFExporter:
    """Clase para exportar datos a PDF"""
    
    @staticmethod
    def export_events(events: List[Dict], filepath: Optional[str] = None) -> Optional[str]:
        """Exporta eventos a PDF. Si no se proporciona filepath, usa diálogo de guardado"""
        if filepath is None:
            # Usar diálogo de guardado
            default_filename = f"eventos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
                initialfile=default_filename,
                title="Guardar eventos como PDF"
            )
            
            if not filepath:  # Usuario canceló
                return None
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            story.append(Paragraph("Listado de Eventos", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            if not events:
                story.append(Paragraph("No hay eventos para mostrar.", styles['Normal']))
            else:
                # Preparar datos de la tabla
                data = [['ID', 'Título', 'Ubicación', 'Fecha Inicio', 'Capacidad', 'Estado']]
                
                for event in events:
                    start_date = event.get('start_datetime', '')
                    if start_date:
                        if isinstance(start_date, datetime):
                            start_date = start_date.strftime('%d/%m/%Y %H:%M')
                        else:
                            start_date = str(start_date)
                    
                    data.append([
                        str(event.get('event_id', '')),
                        event.get('title', '')[:30],  # Limitar longitud
                        event.get('location', '')[:20],
                        start_date,
                        str(event.get('capacity', '')),
                        event.get('status', '')
                    ])
                
                # Crear tabla
                table = Table(data, colWidths=[0.5*inch, 2*inch, 1.5*inch, 1.5*inch, 0.8*inch, 1*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                
                story.append(table)
            
            # Pie de página
            story.append(Spacer(1, 0.3*inch))
            footer = Paragraph(
                f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                styles['Normal']
            )
            story.append(footer)
            
            doc.build(story)
            return filepath
            
        except Exception as e:
            print(f"Error al exportar PDF: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def export_registrations(registrations: List[Dict], filepath: Optional[str] = None) -> Optional[str]:
        """Exporta inscripciones a PDF. Si no se proporciona filepath, usa diálogo de guardado"""
        if filepath is None:
            # Usar diálogo de guardado
            default_filename = f"inscripciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
                initialfile=default_filename,
                title="Guardar inscripciones como PDF"
            )
            
            if not filepath:  # Usuario canceló
                return None
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            story.append(Paragraph("Listado de Inscripciones", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            if not registrations:
                story.append(Paragraph("No hay inscripciones para mostrar.", styles['Normal']))
            else:
                # Preparar datos de la tabla
                data = [['ID Evento', 'Evento', 'Participante', 'Email', 'Fecha Inscripción', 'Estado']]
                
                for reg in registrations:
                    # Formatear fecha
                    fecha = reg.get('Fecha Inscripción', '') or reg.get('registered_at', '')
                    if fecha:
                        if isinstance(fecha, datetime):
                            fecha_str = fecha.strftime('%d/%m/%Y %H:%M')
                        else:
                            try:
                                fecha_str = datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y %H:%M')
                            except:
                                fecha_str = str(fecha)
                    else:
                        fecha_str = ''
                    
                    data.append([
                        str(reg.get('ID Evento', '') or reg.get('event_id', '')),
                        str(reg.get('Evento', '') or reg.get('event_title', ''))[:30],
                        str(reg.get('Participante', '') or f"{reg.get('first_name', '')} {reg.get('last_name', '')}")[:25],
                        str(reg.get('Email', '') or reg.get('email', ''))[:30],
                        fecha_str,
                        str(reg.get('Estado', '') or reg.get('status', 'confirmado'))
                    ])
                
                # Crear tabla
                table = Table(data, colWidths=[0.6*inch, 2*inch, 1.5*inch, 1.8*inch, 1.2*inch, 0.9*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                
                story.append(table)
            
            # Pie de página
            story.append(Spacer(1, 0.3*inch))
            footer = Paragraph(
                f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                styles['Normal']
            )
            story.append(footer)
            
            doc.build(story)
            return filepath
            
        except Exception as e:
            print(f"Error al exportar PDF: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def export_participants(participants: List[Dict], filepath: Optional[str] = None) -> Optional[str]:
        """Exporta participantes a PDF. Si no se proporciona filepath, usa diálogo de guardado"""
        if filepath is None:
            # Usar diálogo de guardado
            default_filename = f"participantes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
                initialfile=default_filename,
                title="Guardar participantes como PDF"
            )
            
            if not filepath:  # Usuario canceló
                return None
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            story.append(Paragraph("Listado de Participantes", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            if not participants:
                story.append(Paragraph("No hay participantes para mostrar.", styles['Normal']))
            else:
                # Preparar datos de la tabla
                data = [['ID', 'Nombre', 'Apellidos', 'Email', 'Teléfono', 'DNI/NIE']]
                
                for participant in participants:
                    data.append([
                        str(participant.get('participant_id', '')),
                        participant.get('first_name', ''),
                        participant.get('last_name', ''),
                        participant.get('email', '')[:30],
                        str(participant.get('phone', '')),
                        participant.get('identifier', '')
                    ])
                
                # Crear tabla
                table = Table(data, colWidths=[0.5*inch, 1.2*inch, 1.5*inch, 2*inch, 1*inch, 1*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                
                story.append(table)
            
            # Pie de página
            story.append(Spacer(1, 0.3*inch))
            footer = Paragraph(
                f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                styles['Normal']
            )
            story.append(footer)
            
            doc.build(story)
            return filepath
            
        except Exception as e:
            print(f"Error al exportar PDF: {e}")
            return None
    
    @staticmethod
    def export_full_report(events: List[Dict], participants: List[Dict], registrations: List[Dict], filepath: Optional[str] = None) -> Optional[str]:
        """Exporta un reporte completo en PDF con eventos, participantes e inscripciones. Si no se proporciona filepath, usa diálogo de guardado"""
        if filepath is None:
            # Usar diálogo de guardado
            default_filename = f"reporte_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
                initialfile=default_filename,
                title="Guardar reporte completo como PDF"
            )
            
            if not filepath:  # Usuario canceló
                return None
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Portada
            title_style = ParagraphStyle(
                'ReportTitle',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=20,
                alignment=TA_CENTER
            )
            
            subtitle_style = ParagraphStyle(
                'ReportSubtitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#666666'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            story.append(Spacer(1, 2*inch))
            story.append(Paragraph("REPORTE COMPLETO", title_style))
            story.append(Paragraph("Gestor de Eventos Locales", subtitle_style))
            story.append(Spacer(1, 0.5*inch))
            story.append(Paragraph(
                f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}",
                styles['Normal']
            ))
            story.append(Spacer(1, 1*inch))
            
            # Resumen/Estadísticas
            summary_style = ParagraphStyle(
                'SummaryTitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=15,
                spaceBefore=20
            )
            
            story.append(Paragraph("RESUMEN GENERAL", summary_style))
            
            # Filtrar eventos cancelados (no se cuentan en el total)
            # Normalizar el status: convertir a string, quitar espacios y convertir a minúsculas
            eventos_no_cancelados = [
                e for e in events 
                if str(e.get('status', '')).strip().lower() != 'cancelado'
            ]
            eventos_cancelados = [
                e for e in events 
                if str(e.get('status', '')).strip().lower() == 'cancelado'
            ]
            
            # Ordenar eventos por ID
            eventos_no_cancelados.sort(key=lambda x: x.get('event_id', 0))
            
            # Calcular estadísticas (excluyendo cancelados del total)
            total_events = len(eventos_no_cancelados)
            total_participants = len(participants)
            total_registrations = len(registrations)
            
            # Contar eventos por estado (solo de los no cancelados)
            # Normalizar el status para la comparación
            eventos_activos = sum(1 for e in eventos_no_cancelados if str(e.get('status', '')).strip().lower() == 'activo')
            eventos_planificados = sum(1 for e in eventos_no_cancelados if str(e.get('status', '')).strip().lower() == 'planificado')
            eventos_finalizados = sum(1 for e in eventos_no_cancelados if str(e.get('status', '')).strip().lower() == 'finalizado')
            
            # Datos del resumen
            summary_data = [
                ['Métrica', 'Cantidad'],
                ['Total de Eventos', str(total_events)],
                ['  - Eventos Activos', str(eventos_activos)],
                ['  - Eventos Planificados', str(eventos_planificados)],
                ['  - Eventos Finalizados', str(eventos_finalizados)],
                ['Total de Participantes', str(total_participants)],
                ['Total de Inscripciones', str(total_registrations)]
            ]
            
            # Agregar eventos cancelados como información adicional si existen
            if eventos_cancelados:
                summary_data.append(['  - Eventos Cancelados (excluidos)', str(len(eventos_cancelados))])
            
            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.5*inch))
            
            # Sección de Eventos
            section_style = ParagraphStyle(
                'SectionTitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=15,
                spaceBefore=20
            )
            
            story.append(Paragraph("EVENTOS", section_style))
            
            if not eventos_no_cancelados:
                story.append(Paragraph("No hay eventos registrados.", styles['Normal']))
            else:
                # Preparar datos de eventos (solo eventos no cancelados)
                events_data = [['ID', 'Título', 'Ubicación', 'Fecha Inicio', 'Capacidad', 'Estado']]
                
                for event in eventos_no_cancelados:
                    start_date = event.get('start_datetime', '')
                    if start_date:
                        if isinstance(start_date, datetime):
                            start_date = start_date.strftime('%d/%m/%Y %H:%M')
                        else:
                            try:
                                start_date = datetime.strptime(str(start_date), "%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y %H:%M')
                            except:
                                start_date = str(start_date)
                    
                    events_data.append([
                        str(event.get('event_id', '')),
                        event.get('title', '')[:30],
                        event.get('location', '')[:20],
                        start_date,
                        str(event.get('capacity', '')),
                        event.get('status', '')
                    ])
                
                events_table = Table(events_data, colWidths=[0.5*inch, 2*inch, 1.5*inch, 1.5*inch, 0.8*inch, 1*inch])
                events_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                
                story.append(events_table)
            
            story.append(Spacer(1, 0.4*inch))
            
            # Sección de Participantes
            story.append(Paragraph("PARTICIPANTES", section_style))
            
            if not participants:
                story.append(Paragraph("No hay participantes registrados.", styles['Normal']))
            else:
                # Ordenar participantes por ID
                participants_sorted = sorted(participants, key=lambda x: x.get('participant_id', 0))
                
                # Preparar datos de participantes
                participants_data = [['ID', 'Nombre', 'Apellidos', 'Email', 'Teléfono', 'DNI/NIE']]
                
                for participant in participants_sorted:
                    participants_data.append([
                        str(participant.get('participant_id', '')),
                        participant.get('first_name', ''),
                        participant.get('last_name', ''),
                        participant.get('email', '')[:30],
                        str(participant.get('phone', '')),
                        participant.get('identifier', '')
                    ])
                
                participants_table = Table(participants_data, colWidths=[0.5*inch, 1.2*inch, 1.5*inch, 2*inch, 1*inch, 1*inch])
                participants_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                ]))
                
                story.append(participants_table)
            
            story.append(Spacer(1, 0.4*inch))
            
            # Sección de Inscripciones
            story.append(Paragraph("INSCRIPCIONES", section_style))
            
            if not registrations:
                story.append(Paragraph("No hay inscripciones registradas.", styles['Normal']))
            else:
                # Ordenar inscripciones por ID Evento
                registrations_sorted = sorted(registrations, key=lambda x: int(x.get('ID Evento', 0) or x.get('event_id', 0) or 0))
                
                # Preparar datos de inscripciones
                registrations_data = [['ID Evento', 'Evento', 'Participante', 'Email', 'Fecha Inscripción', 'Estado']]
                
                for reg in registrations_sorted:
                    # Formatear fecha
                    fecha = reg.get('Fecha Inscripción', '') or reg.get('registered_at', '')
                    if fecha:
                        if isinstance(fecha, datetime):
                            fecha_str = fecha.strftime('%d/%m/%Y %H:%M')
                        else:
                            try:
                                fecha_str = datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y %H:%M')
                            except:
                                fecha_str = str(fecha)
                    else:
                        fecha_str = ''
                    
                    registrations_data.append([
                        str(reg.get('ID Evento', '') or reg.get('event_id', '')),
                        str(reg.get('Evento', '') or reg.get('event_title', ''))[:30],
                        str(reg.get('Participante', '') or f"{reg.get('first_name', '')} {reg.get('last_name', '')}")[:25],
                        str(reg.get('Email', '') or reg.get('email', ''))[:30],
                        fecha_str,
                        str(reg.get('Estado', '') or reg.get('status', 'confirmado'))
                    ])
                
                registrations_table = Table(registrations_data, colWidths=[0.6*inch, 2*inch, 1.5*inch, 1.8*inch, 1.2*inch, 0.9*inch])
                registrations_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 7),
                ]))
                
                story.append(registrations_table)
            
            # Pie de página
            story.append(Spacer(1, 0.5*inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#666666'),
                alignment=TA_CENTER
            )
            footer = Paragraph(
                f"Reporte generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Gestor de Eventos Locales",
                footer_style
            )
            story.append(footer)
            
            doc.build(story)
            return filepath
            
        except Exception as e:
            print(f"Error al exportar reporte completo: {e}")
            import traceback
            traceback.print_exc()
            return None

