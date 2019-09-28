def template_content(brand, year, engine, price, export, difference, link, site):
    content = f'Marka: {str(brand)}\nRocznik: {year}\nSilnik: {engine}\nCena :{price}\n' \
              f'Cena na eksport: {export}\nRóżnica cen: {difference}\nLink: {site}{link}'
    return content
