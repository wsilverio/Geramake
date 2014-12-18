#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os, errno

print "\n### GERAMAKE ###\n"

def openDir(dir):
    try:
        # navega até o diretório do projeto
        os.chdir(dir)
    except OSError as e:
        if e.errno == errno.ENOENT:
            # diretório não encontrado
            print "Diretório não encontrado"
            print "Tente $ python geramake.py \"diretorio\"\n"
            exit()
        else:
            print e
            exit()

def openBuild(dir):
    try:
        # navega até o diretório de compilação
        os.chdir(dir + "/build")
        return 0

    except OSError as e:
        if e.errno == errno.ENOENT:
            # diretório não encontrado
            print "Diretório \"build\" não encontrado."
            return 1
        else:
            print e
            exit()

def getProjName():
    print "Procurando por CMakeLists.txt ..."
    try:
        # busca o nome do projeto no arquivo CMakeLists.txt
        with open('CMakeLists.txt', 'r') as cmklist:
            print "CMakeLists.txt encontrado.\nBuscando pelo nome do projeto."
            for linha in cmklist:
                if 'project(' in linha:
                    # obtem o nome do projeto na linha: project(Nome do projeto)
                    name = linha[len('project('):-2]
                    print "Projeto: %s\n" %name
                    return name
    except IOError as e:
        if e.errno == errno.ENOENT:
            # arquivo CMakeLists.txt não encontrado
            print "CMakeLists.txt não encontrado."
            print "Tente $ python geramake.py \"diretorio\" \"nome do projeto\" para gerar o CMakeLists.txt\n"
            return 1
        else:
            print e
            exit()

def criaBuild(dir):
    try:
        os.mkdir(dir + "/build", 0755)
    except OSError as e:
        if e.errno == errno.EACCES:
            print "Erro ao criar %s/build" %dir
            print "Permissão negada."
            exit()
        elif e.errno == errno.EEXIST:
            print "Diretório %s/build já existe." %dir
        else:
            print e
            exit()

def cmake(dir):
    try:
        os.system('cmake %s' %dir)
    except e:
        print e
        exit()

def make():
    try:
        os.system('make')
    except e:
        print e
        exit()

def linkFile(src, dst):
    try:
        os.link(src, dst + src)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            print e
            exit()

def criaCMakeLists(project):
    try:
        file = open("CMakeLists.txt", 'w')
        file.write(
            "cmake_minimum_required( VERSION 2.8 )\n"
            "project(%s)\n"
            "file( GLOB SRCS *.cpp )\n"
            "file( GLOB HEADERS *.h )\n"
            "set( CMAKE_C_FLAGS \"${CMAKE_C_FLAGS} `pkg-config --cflags --libs opencv`\" )\n"
            "find_package( OpenCV REQUIRED )\n"
            "add_executable( ${CMAKE_PROJECT_NAME} ${SRCS} ${HEADERS} )\n"
            "target_link_libraries( ${CMAKE_PROJECT_NAME} ${OpenCV_LIBS} )\n"
            %project
        )
    except OSError as e:
        if e.errno == errno.EACCES:
            print "Erro ao criar CMakeLists.txt"
            print "Permissão negada."
            exit()
        elif e.errno == errno.EEXIST:
            print "CMakeLists.txt já existe."
        else:
            print e
            exit()

def run(file):
    print "\nExecutando arquivo ./%s" %file

    teste = os.system("./" + file)
    if teste != 0:
        print file, "não encontrado"

def main():
    diretorio = sys.argv[1]

    # make, run
    if len(sys.argv) == 2:

        # abre o arquivo CMakeLists.txt
        project = getProjName()

        # se o CMakeLists existir
        if project != 1:

            # abre o diretório do projeto
            openDir(diretorio)

            # verifica se o diretório 'build'
            if openBuild(diretorio) == 0:
                cmake("../")
                make()
                openDir(diretorio)
                run(project)
            else:
                # build não encontrado
                # cria o diretório build
                criaBuild(diretorio)
                openBuild(diretorio)
                cmake("../")
                make()
                linkFile(project, "../")
                openDir(diretorio)
                run(project)

    # cmake, make, run
    elif len(sys.argv) == 3:

        openDir(diretorio)

        project = getProjName()

        # CMakeLists.txt encontrado
        if project != 1:
            key = raw_input("Deseja substituir (s/n)?: ")
            if key.upper() != 'S':
                print "Nada a ser feito."
                print "Para compilar, tente\nTente $ python geramake.py \"diretorio\""
                exit()

        # cria CMakeLists.txt

        project = sys.argv[2]

        try:
            os.remove("CMakeLists.txt")
        except OSError as e:
            if e.errno == errno.ENOENT:
                pass
            else:
                print e
                exit()

        criaCMakeLists(project)

        if openBuild(diretorio) == 0:
            cmake("../")
            make()
            linkFile(project, "../")
            openDir(diretorio)
            run(project)
        else:
            # build não encontrado
            # cria o diretório build
            criaBuild(diretorio)
            openBuild(diretorio)
            cmake("../")
            make()
            linkFile(project, "../")
            openDir(diretorio)
            run(project)

    else:
        print "Parâmetros inválidos."
        print "Tente $ python geramake.py \"diretorio\""
        print "Ou    $ python geramake.py \"diretorio\" \"nome do projeto\"\n"
        exit()

if __name__ == "__main__":
    main()