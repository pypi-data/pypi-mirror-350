from setuptools import setup

setup(name='shells_cae',
      version='0.0.36',
      description='Special CAЕ Library by sabbraxcaddabra&denchina',
      packages=['shells_cae', 'shells_cae.optimizers'],
      package_data={'shells_cae':[
            'compiled/al_tate_model/src/*.f90',
            'compiled/al_tate_model/CMakeLists.txt',
            'compiled/external_ballistics/src/*.f90',
            'compiled/external_ballistics/CMakeLists.txt',
            'compiled/internal_ballistics/src/*.f90',
            'compiled/internal_ballistics/CMakeLists.txt',
            'compiled/mcdrag/src/*.f90',
            'compiled/mcdrag/CMakeLists.txt',
            'compiled/kontur/include/*.h',
            'compiled/kontur/src/*.for',
            'compiled/kontur/src/*.c',
            'compiled/kontur/CMakeLists.txt',
            'compiled/build/bin/*.*',
            'compiled/build/bin/lib/*.so',
            'compiled/Spin73/*.*',
            'compiled/external_3D_ballistics/ballistics3D.dll',
      ]},


      author_email='denisdoronichev@outlook.com',
      include_package_data=True,
      zip_safe=False,
      install_requires=['numpy>=1.23.4', 'cffi>=1.15.1'],
      python_requires='>=3.11'
      )


# Команда для обновления файлов сборки
# python setup.py sdist

# Отправка на сервер новой версии
# twine upload dist/*


