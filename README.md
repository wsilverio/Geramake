Gera o **CMakeLists.txt** para os experimentos com openCV

#### Arquivos de teste
- teste_gauss/filtro_gauss_trackbar.cpp  
- teste_gauss/Fig0340(a)(dipxe_text).tif

#### uso
**Para gerar o CMakeLists.txt:**
```bash
$ python geramake.py [caminho] [nomeProjeto]
```
Exemplo:
```bash
$ python geramake.py teste_gauss/ gaussTrackbar
```
Gerado
- teste_gauss/CMakeLists.txt

**Para compilar e executar o programa:**
```bash
$ python geramake.py [caminho]
```
Exemplo:
```bash
$ python geramake.py teste_gauss/
```
Gerado:
- teste_gauss/build/
- teste_gauss/gaussTrackbar.run