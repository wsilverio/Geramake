#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os, errno
from unicodedata import normalize

print "\n### GERAMAKE ###\n"

printFun = False

def rmBkspace(txt):
    return txt.replace(' ', '_')

def openDir(dir):
    if printFun: print "openDir()", dir
    try:
        # navega até o diretório do projeto
        os.chdir(dir)
        return 0
    except OSError as e:
        if e.errno == errno.ENOENT:
            # diretório não encontrado
            print "Diretório não encontrado"
            print "Tente $ python geramake.py \"diretorio\"\n"
            return 1
        else:
            print e
            exit()

def getProjName():
    if printFun: print "getProjName()"
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
            print "Tente\n$ python geramake.py \"diretorio\" \"nome do projeto\"\npara gerar o CMakeLists.txt\n"
            return 1
        else:
            print e
            exit()

def mkDir(dir):
    if printFun: print "mkDir()"
    try:
        os.mkdir(dir, 0755)
    except OSError as e:
        if e.errno == errno.EACCES:
            print "Erro ao criar %sbuild" %dir
            print "Permissão negada."
            exit()
        elif e.errno == errno.EEXIST:
            print "Diretório %sbuild já existe." %dir
        else:
            print e
            exit()

def cmake(dir):
    if printFun: print "cmake()"
    try:
        os.system('cmake %s' %dir)
    except Exception as e:
        print e
        exit()

def make():
    if printFun: print "make()"
    try:
        os.system('make')
    except Exception as e:
        print e
        exit()

def linkFile(src, dst):
    if printFun: print "linkFile()"
    try:
        os.link(src, dst + src + ".run")
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            print e
            exit()

def createCMakeLists(project):
    if printFun: print "createCMakeLists()"
    try:
        file = open("CMakeLists.txt", 'w')
        file.write(
            "cmake_minimum_required( VERSION 2.8 )\n"
            "project(%s)\n"
            "file( GLOB SRCS *.cpp )\n"
            "file( GLOB HEADERS *.h )\n"
            "set( CMAKE_CXX_FLAGS \"${CMAKE_CXX_FLAGS} -std=c++11\" )\n"
            "find_package( OpenCV REQUIRED )\n"
            "add_executable( ${CMAKE_PROJECT_NAME} ${SRCS} ${HEADERS} )\n"
            "target_link_libraries( ${CMAKE_PROJECT_NAME} ${OpenCV_LIBS} )\n"
            %project
        )
        print "CMakeLists.txt criado."
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
    if printFun: print "run()"
    print "\nExecutando arquivo ./%s" %file

    teste = os.system("./" + file)
    if teste != 0:
        print file, "não encontrado"

def main():

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Parâmetros inválidos."
        print "Tente $ python geramake.py \"diretorio\""
        print "Ou    $ python geramake.py \"diretorio\" \"nome do projeto\"\n"
        exit()

    else:

        diretorio = sys.argv[1]

        # abre o diretório do projeto
        openDir(diretorio)

        # abre o arquivo CMakeLists.txt
        project = getProjName()

        # make, run
        if len(sys.argv) == 2:

            # se o CMakeLists existir
            if project != 1:

                # verifica se o diretório 'build'
                if openDir("build") == 0:
                    cmake("../")
                    make()
                    linkFile(project, "../")
                    openDir("../")
                    run(project)
                else:
                    # build não encontrado
                    # cria o diretório build
                    mkDir("build")
                    openDir("build")
                    cmake("../")
                    make()
                    linkFile(project, "../")
                    openDir(diretorio)
                    run(project)


        # cmake, make, run
        elif len(sys.argv) == 3:

            # CMakeLists.txt encontrado
            if project != 1:
                key = raw_input("Deseja substituir (s/n)?: ").upper()
                if key == 'N':
                    pass
                elif key == 'S':

                    try:
                        os.remove("CMakeLists.txt")
                    except OSError as e:
                        if e.errno == errno.ENOENT:
                            pass
                        else:
                            print e
                            exit()

                    project = rmBkspace(sys.argv[2])

                    # cria CMakeLists.txt
                    createCMakeLists(project)

                else:
                    print "Nada a ser feito."
                    exit()

            else:
                project = rmBkspace(sys.argv[2])
                # cria CMakeLists.txt
                createCMakeLists(project)

            if raw_input("Deseja compliar e executar o programa? (s/n): ").upper() != 'S':
                exit()

            if openDir("build") == 0:
                cmake("../")
                make()
                linkFile(project, "../")
                openDir("../")
                run(project + ".run")
            else:
                # build não encontrado
                # cria o diretório build
                mkDir("build")
                openDir("build")
                cmake("../")
                make()
                linkFile(project, "../")
                openDir("../")
                run(project + ".run")


if __name__ == "__main__":
    main()