#!/usr/bin/env python3
"""
Script para analizar la estructura de los archivos XLSB de reportes
"""
from pyxlsb import open_workbook
from pathlib import Path

def analyze_xlsb(file_path):
    """Analiza un archivo XLSB y muestra su estructura"""
    print(f"\n{'='*80}")
    print(f"Analizando: {Path(file_path).name}")
    print(f"{'='*80}\n")

    try:
        with open_workbook(file_path) as wb:
            print(f"Número de hojas: {len(wb.sheets)}")
            print(f"\nHojas: {', '.join(wb.sheets)}")

            # Analizar cada hoja
            for sheet_name in wb.sheets:
                print(f"\n{'-'*80}")
                print(f"Hoja: '{sheet_name}'")
                print(f"{'-'*80}")

                with wb.get_sheet(sheet_name) as sheet:
                    rows = []
                    formulas = []
                    row_count = 0

                    # Leer las primeras 50 filas
                    for row in sheet.rows():
                        row_count += 1
                        if row_count <= 20:  # Guardar primeras 20 filas
                            row_values = []
                            for col_idx, cell in enumerate(row):
                                if cell.v is not None:
                                    # Detectar si es una fórmula (aproximación: empieza con =)
                                    cell_str = str(cell.v)
                                    if cell_str.startswith('='):
                                        formulas.append({
                                            'row': row_count,
                                            'col': col_idx + 1,
                                            'formula': cell_str[:100]
                                        })
                                        row_values.append(f"[FORMULA]")
                                    else:
                                        row_values.append(cell_str[:30])
                                else:
                                    row_values.append("")

                            rows.append(row_values)

                        if row_count > 100:
                            # Solo contar el resto
                            for cell in row:
                                if cell.v and str(cell.v).startswith('=') and len(formulas) < 50:
                                    formulas.append({
                                        'row': row_count,
                                        'col': 0,
                                        'formula': str(cell.v)[:100]
                                    })

                    print(f"Filas procesadas: {row_count}")

                    if formulas:
                        print(f"\nFórmulas encontradas (muestra de primeras {min(len(formulas), 15)}):")
                        for f in formulas[:15]:
                            print(f"  Fila {f['row']}, Col {f['col']}: {f['formula']}")
                        if len(formulas) > 15:
                            print(f"  ... y {len(formulas) - 15} más")

                    # Mostrar las primeras filas
                    print(f"\nPrimeras 10 filas (muestra):")
                    for idx, row_data in enumerate(rows[:10], start=1):
                        # Mostrar solo las primeras 8 columnas
                        display_data = row_data[:8]
                        if display_data:
                            print(f"  Fila {idx}: {' | '.join(display_data)}")

    except Exception as e:
        print(f"Error al analizar {file_path}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reportes_dir = Path("exampleclaude/reportes")

    excel_files = [
        reportes_dir / "Trayectoria online LL.xlsb",
        reportes_dir / "Trayectoria online EL.xlsb",
        reportes_dir / "Trayectoria online ML.xlsb"
    ]

    for excel_file in excel_files:
        if excel_file.exists():
            analyze_xlsb(excel_file)
        else:
            print(f"Archivo no encontrado: {excel_file}")
