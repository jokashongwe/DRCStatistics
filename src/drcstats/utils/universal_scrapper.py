from bs4 import BeautifulSoup
import json
from pathlib import Path

def universal_parser(text: str, filename: str):
    soup = BeautifulSoup(text, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        heads = table.find_all('th')
        keys = [head.text for head in heads]
        lines = table.find_all('tr')
        size = len(keys)
        file_path = Path(filename)
        if not file_path.parent.exists():
            file_path.parent.mkdir()
        with open(filename, 'a+', encoding='utf-8') as file:
            for line in lines:
                cells = line.find_all('td')
                obj = {}
                for i in range(size):
                    obj[keys[i]] = cells[i].text
                file.write(json.dumps(obj, ensure_ascii=False) + "\n")
                    
                

if __name__ =="__main__":
    html = """
        <table class="table" width="100%" border="0" cellspacing="0" cellpadding="0"><thead class="tableheader"><tr><th align="center" bgcolor="#f8f8f8" style="border-right:1px solid #d4d4d4; text-align:center;"></th><th class="lt_pad">Company Name</th><th class="lt_pad">Street</th><th class="lt_pad">City</th><th class="lt_pad">Country</th><th class="lt_pad">Website</th><th class="lt_pad">Phone</th><th class="lt_pad">Contact&nbsp;Person</th><th class="lt_pad">Email</th></tr></thead><tbody><tr><td align="center" bgcolor="#f8f8f8"> 1</td><td class="td_cinx_cname"><div class="hoverlink" row-id="206690319"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="L`homme Vaidoso">L`homme Vaidoso</div></a></div></td><td class="pad_lt td_cinx_street"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_city"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="http://www.lhomme.ao/" style="cursor:pointer;" href="http://www.lhomme.ao/" target="_blank">lhomme.ao</a></div></td><td class="pad_lt td_cinx_phone" title="+244 927062065"><div class="cmp_clmn_dots">+244 927062065</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title="info@lhomme.ao"><div class="cmp_clmn_dots"><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="d3babdb5bc93bfbbbcbebeb6fdb2bc">[email&nbsp;protected]</a></div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 2</td><td class="td_cinx_cname"><div class="hoverlink" row-id="208033471"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Perfumaria Benga Cosméticos">Perfumaria Benga Cosméticos</div></a></div></td><td class="pad_lt td_cinx_street" title="Lar do Patriota, Estr. Lar Patriota"><div class="cmp_clmn_dots">Lar do Patriota, Estr. Lar Patriota</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://www.instagram.com/bengacosmeticos/" style="cursor:pointer;" href="https://www.instagram.com/bengacosmeticos/" target="_blank">instagram.com</a></div></td><td class="pad_lt td_cinx_phone" title="+244 940280989"><div class="cmp_clmn_dots">+244 940280989</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title="patrickcholewa@hotmail.com"><div class="cmp_clmn_dots"><a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="bcccddc8ced5dfd7dfd4d3d0d9cbddfcd4d3c8d1ddd5d092dfd3d1">[email&nbsp;protected]</a></div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 3</td><td class="td_cinx_cname"><div class="hoverlink" row-id="205792625"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Longrich Cosméticos">Longrich Cosméticos</div></a></div></td><td class="pad_lt td_cinx_street" title="Grafanil bar"><div class="cmp_clmn_dots">Grafanil bar</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://xn--longrich-cosmticos-nwb.negocio.site/" style="cursor:pointer;" href="https://xn--longrich-cosmticos-nwb.negocio.site/" target="_blank">xn--longrich-cosmticos-nwb.negocio.site</a></div></td><td class="pad_lt td_cinx_phone" title="+244 931884852"><div class="cmp_clmn_dots">+244 931884852</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 4</td><td class="td_cinx_cname"><div class="hoverlink" row-id="205812057"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Best Market">Best Market</div></a></div></td><td class="pad_lt td_cinx_street" title="Brico, Avenida Deolinda Rodrigues Nº 24 Palanca,entrada da Rua H(junto a"><div class="cmp_clmn_dots">Brico, Avenida Deolinda Rodrigues Nº 24 Palanca,entrada da Rua H(junto a</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://bestmarket.co.ao/" style="cursor:pointer;" href="https://bestmarket.co.ao/" target="_blank">bestmarket.co.ao</a></div></td><td class="pad_lt td_cinx_phone" title="+244 912909090"><div class="cmp_clmn_dots">+244 912909090</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 5</td><td class="td_cinx_cname"><div class="hoverlink" row-id="205829067"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Probeauty Industria De Cosmeticos">Probeauty Industria De Cosmeticos</div></a></div></td><td class="pad_lt td_cinx_street" title="Bairro das Tendas Benfica"><div class="cmp_clmn_dots">Bairro das Tendas Benfica</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="http://www.probeautyind.ao/" style="cursor:pointer;" href="http://www.probeautyind.ao/" target="_blank">probeautyind.ao</a></div></td><td class="pad_lt td_cinx_phone" title="+244 925561332"><div class="cmp_clmn_dots">+244 925561332</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 6</td><td class="td_cinx_cname"><div class="hoverlink" row-id="205467260"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Avon Angola">Avon Angola</div></a></div></td><td class="pad_lt td_cinx_street" title="Condominio Espaços Avenida Edificio Beta Loja Nr.14/15. Bairro, Av. Talatona"><div class="cmp_clmn_dots">Condominio Espaços Avenida Edificio Beta Loja Nr.14/15. Bairro, Av. Talatona</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://avon.co.ao/" style="cursor:pointer;" href="https://avon.co.ao/" target="_blank">avon.co.ao</a></div></td><td class="pad_lt td_cinx_phone" title="+244 947837176"><div class="cmp_clmn_dots">+244 947837176</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 7</td><td class="td_cinx_cname"><div class="hoverlink" row-id="205459096"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Baobá Online">Baobá Online</div></a></div></td><td class="pad_lt td_cinx_street"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_city"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://baoba-online.negocio.site/" style="cursor:pointer;" href="https://baoba-online.negocio.site/" target="_blank">baoba-online.negocio.site</a></div></td><td class="pad_lt td_cinx_phone" title="+244 921479600"><div class="cmp_clmn_dots">+244 921479600</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 8</td><td class="td_cinx_cname"><div class="hoverlink" row-id="205392276"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Angotarew Comércio E Serviços Ltd">Angotarew Comércio E Serviços Ltd</div></a></div></td><td class="pad_lt td_cinx_street" title="R. D do Morro Bento"><div class="cmp_clmn_dots">R. D do Morro Bento</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="http://angotarew.comercio.com/" style="cursor:pointer;" href="http://angotarew.comercio.com/" target="_blank">angotarew.comercio.com</a></div></td><td class="pad_lt td_cinx_phone" title="+244 934249189"><div class="cmp_clmn_dots">+244 934249189</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 9</td><td class="td_cinx_cname"><div class="hoverlink" row-id="206054930"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Tudoaqui">Tudoaqui</div></a></div></td><td class="pad_lt td_cinx_street" title="espaço casa, Avenida 21 de janeiro Morro Bento junto"><div class="cmp_clmn_dots">espaço casa, Avenida 21 de janeiro Morro Bento junto</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="http://tudoaqui.co.ao/" style="cursor:pointer;" href="http://tudoaqui.co.ao/" target="_blank">tudoaqui.co.ao</a></div></td><td class="pad_lt td_cinx_phone" title="+244 932218922"><div class="cmp_clmn_dots">+244 932218922</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 10</td><td class="td_cinx_cname"><div class="hoverlink" row-id="206322657"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Bavuidi Services">Bavuidi Services</div></a></div></td><td class="pad_lt td_cinx_street" title="Alfa 5 Cazenga"><div class="cmp_clmn_dots">Alfa 5 Cazenga</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://bavuidi-services-cosmetics.negocio.site/" style="cursor:pointer;" href="https://bavuidi-services-cosmetics.negocio.site/" target="_blank">bavuidi-services-cosmetics.negocio.site</a></div></td><td class="pad_lt td_cinx_phone" title="+244 943885438"><div class="cmp_clmn_dots">+244 943885438</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 11</td><td class="td_cinx_cname"><div class="hoverlink" row-id="206338154"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Sao Paulo Market">Sao Paulo Market</div></a></div></td><td class="pad_lt td_cinx_street" title="57P5Q44"><div class="cmp_clmn_dots">57P5Q44</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="http://srdanielcosmeticos.ao/" style="cursor:pointer;" href="http://srdanielcosmeticos.ao/" target="_blank">srdanielcosmeticos.ao</a></div></td><td class="pad_lt td_cinx_phone" title="+244 923953962"><div class="cmp_clmn_dots">+244 923953962</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 12</td><td class="td_cinx_cname"><div class="hoverlink" row-id="206706709"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Ftv Comestics Angola">Ftv Comestics Angola</div></a></div></td><td class="pad_lt td_cinx_street" title="Rua Rainha Ginga, Torre Elysée n 29, R/C, Ingombota"><div class="cmp_clmn_dots">Rua Rainha Ginga, Torre Elysée n 29, R/C, Ingombota</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="http://www.ftv-angola.com/" style="cursor:pointer;" href="http://www.ftv-angola.com/" target="_blank">ftv-angola.com</a></div></td><td class="pad_lt td_cinx_phone" title="+244 928979361"><div class="cmp_clmn_dots">+244 928979361</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 13</td><td class="td_cinx_cname"><div class="hoverlink" row-id="206707427"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Maria Luís Cosméticos">Maria Luís Cosméticos</div></a></div></td><td class="pad_lt td_cinx_street"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_city"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://maria-leo-longrich.negocio.site/" style="cursor:pointer;" href="https://maria-leo-longrich.negocio.site/" target="_blank">maria-leo-longrich.negocio.site</a></div></td><td class="pad_lt td_cinx_phone" title="+244 943956669"><div class="cmp_clmn_dots">+244 943956669</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 14</td><td class="td_cinx_cname"><div class="hoverlink" row-id="207220819"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Natural Beauty">Natural Beauty</div></a></div></td><td class="pad_lt td_cinx_street" title="R. Bula Matadi 96"><div class="cmp_clmn_dots">R. Bula Matadi 96</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="http://www.naturalbeautyangola.com/" style="cursor:pointer;" href="http://www.naturalbeautyangola.com/" target="_blank">naturalbeautyangola.com</a></div></td><td class="pad_lt td_cinx_phone" title="+244 922192466"><div class="cmp_clmn_dots">+244 922192466</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 15</td><td class="td_cinx_cname"><div class="hoverlink" row-id="207955880"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Avon Nancia">Avon Nancia</div></a></div></td><td class="pad_lt td_cinx_street" title="Rua Olímpio Macueira"><div class="cmp_clmn_dots">Rua Olímpio Macueira</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="http://www.avonnancia.com/" style="cursor:pointer;" href="http://www.avonnancia.com/" target="_blank">avonnancia.com</a></div></td><td class="pad_lt td_cinx_phone" title="+244 923584315"><div class="cmp_clmn_dots">+244 923584315</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 16</td><td class="td_cinx_cname"><div class="hoverlink" row-id="208335491"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Bavuidiservices">Bavuidiservices</div></a></div></td><td class="pad_lt td_cinx_street" title="Bairro Cazenga Asa branca"><div class="cmp_clmn_dots">Bairro Cazenga Asa branca</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://bavuidiservices-cosmetics-and-parfumes-supplier.negocio.site/" style="cursor:pointer;" href="https://bavuidiservices-cosmetics-and-parfumes-supplier.negocio.site/" target="_blank">bavuidiservices-cosmetics-and-parfumes-supplier.negocio.site</a></div></td><td class="pad_lt td_cinx_phone" title="+244 943885438"><div class="cmp_clmn_dots">+244 943885438</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 17</td><td class="td_cinx_cname"><div class="hoverlink" row-id="208372346"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Miraldina Cosméticos">Miraldina Cosméticos</div></a></div></td><td class="pad_lt td_cinx_street"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_city"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://miraldina-cosmeticos.negocio.site/" style="cursor:pointer;" href="https://miraldina-cosmeticos.negocio.site/" target="_blank">miraldina-cosmeticos.negocio.site</a></div></td><td class="pad_lt td_cinx_phone" title="+244 927992644"><div class="cmp_clmn_dots">+244 927992644</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 18</td><td class="td_cinx_cname"><div class="hoverlink" row-id="208525318"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="J.B.Cosméticos">J.B.Cosméticos</div></a></div></td><td class="pad_lt td_cinx_street"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_city"><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://mayetujo.negocio.site/?" style="cursor:pointer;" href="https://mayetujo.negocio.site/?" target="_blank">mayetujo.negocio.site</a></div></td><td class="pad_lt td_cinx_phone" title="+244 999673957"><div class="cmp_clmn_dots">+244 999673957</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 19</td><td class="td_cinx_cname"><div class="hoverlink" row-id="208773261"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Virgin Hair Fabulous Wig">Virgin Hair Fabulous Wig</div></a></div></td><td class="pad_lt td_cinx_street" title="Museum of Natural History, Rua da Missão, Kinaxixi antes cruzamento"><div class="cmp_clmn_dots">Museum of Natural History, Rua da Missão, Kinaxixi antes cruzamento</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://virginhairfabulouswigs.com/" style="cursor:pointer;" href="https://virginhairfabulouswigs.com/" target="_blank">virginhairfabulouswigs.com</a></div></td><td class="pad_lt td_cinx_phone" title="+244 928071027"><div class="cmp_clmn_dots">+244 928071027</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr><tr><td align="center" bgcolor="#f8f8f8"> 20</td><td class="td_cinx_cname"><div class="hoverlink" row-id="209356040"><a href="#" class="cls_cursor_pointer"><div class="c_name cmp_clmn_dots" title="Art Hub">Art Hub</div></a></div></td><td class="pad_lt td_cinx_street" title="Rua Mamã Gorda, Viana Estalagem"><div class="cmp_clmn_dots">Rua Mamã Gorda, Viana Estalagem</div></td><td class="pad_lt td_cinx_city" title="Luanda"><div class="cmp_clmn_dots">Luanda</div></td><td class="pad_lt"><i class="flags_icons_new"><img alt="flags_icons_new" src="https://www.fastbase.com/assets_leads_navigator/images/flags/AO.svg" onerror="_fn_error_on_img(this)"></i><span class="cls_ccode">AO</span></td><td class="pad_lt td_cinx_web"><div class="cmp_clmn_dots"><a class="cls_pointer" title="https://art-hub-cosmetics-and-parfumes-supplier.negocio.site/" style="cursor:pointer;" href="https://art-hub-cosmetics-and-parfumes-supplier.negocio.site/" target="_blank">art-hub-cosmetics-and-parfumes-supplier.negocio.site</a></div></td><td class="pad_lt td_cinx_phone" title="+244 928089114"><div class="cmp_clmn_dots">+244 928089114</div></td><td class="pad_lt td_cinx_con_per" title=""><div class="cmp_clmn_dots">N/A</div></td><td class="pad_lt td_cinx_email" title=""><div class="cmp_clmn_dots">N/A</div></td></tr></tbody></table>
    """
    universal_parser(html, filename="generated/demo/alcor.json")