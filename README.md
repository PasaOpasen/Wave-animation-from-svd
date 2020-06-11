# Wave animation from svd
Unpack svd files and creating animation of running waves.

## Before running

1. Download and install [service tool Polytec Update](http://swdownload.polytec.com/polyupdate/PolytecUpdateSetup.exe)

2. Run it, check **File Access** and **Scan Viewer** and install

3. Download and install [.NET Core>=3.1](https://dotnet.microsoft.com/download)

3. Download [Python](https://www.python.org/downloads/), install with adding to PATH and so on

4. Open **cmd.exe** and run these commands:

```
pip install numpy
pip install matplotlib
```


## По поводу алгоритма

1. Выбираются нужные директории для сохранения в целевой файл

2. Туда копируются скрипты и вспомогательные файлы

3. Запускается [**create.py**](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/target/create.py). Если нужно поменять какие-то параметры изображений, в скрипте это легко делается (в том числе [цветовая палитра](https://matplotlib.org/3.2.1/tutorials/colors/colormaps.html)). Суть скрипта:
  
    1. Сначала информация из целевого файла конвертируется в массивы numpy (может занять минуту)
  
    2. Выводится некоторое описание, после чего **в окне скрипта надо указать шаг по времени** (чтобы не делать рисунки для всех тысяч времён)
  
    3. Создаются рисунки со скоростью примерно 1.5 в секунду (при dpi = 350) на стандартном Python. На анаконде это работает раза в 2-3 быстрее, но ей тяжело пользоваться в рамках общего приложения + много весит

4. После работы скрипта открывается форма, в неё загружаются созданные изображения. 

    * При режиме *скорость* это может занять несколько секунд и около 8Гб оперативки для 500 изображений при dpi = 350 (это больше проблема .NET, так что от разрешения вряд ли есть особая зависимость, поэтому создавать больше 100-200 изображений в этом режиме не рекомендую), зато сам просмотр изображений работает очень быстро и симпатично. 
  
    * При режиме *экономия памяти* изображения считываются по мере надобности + вызвается сборщик мусора. Очень рекомендую использовать этот вариант, так как потери в скорости незаметны.
  
## Example

**Start:**

![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/gifs/start.gif)

**Result 1.0.0:**

![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/gifs/result.gif)

**Result 1.1.0:**

![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/gifs/result2.gif)













