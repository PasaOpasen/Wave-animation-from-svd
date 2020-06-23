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
  
    3. Создаются рисунки со скоростью примерно 1.5 в секунду (при dpi = 350) на стандартном Python. На анаконде это работает раза в 2-3 быстрее, но ей тяжело пользоваться в рамках общего приложения + много весит. Параллелить здесь особо нечего, так как самих вычислений почти нет, время тратится либо на взаимодействие с COM-объектами, либо на графическую панель.

4. После работы скрипта открывается форма, в неё загружаются созданные изображения. 

    * При режиме *скорость* это может занять несколько секунд и около 8Гб оперативки для 500 изображений при dpi = 350 (это больше проблема .NET, так что от разрешения вряд ли есть особая зависимость, поэтому создавать больше 100-200 изображений в этом режиме не рекомендую), зато сам просмотр изображений работает очень быстро и симпатично. 
  
    * При режиме *экономия памяти* изображения считываются по мере надобности + вызвается сборщик мусора. Очень рекомендую использовать этот вариант, так как потери в скорости незаметны.

## Как (предположительно) этим следует пользоваться

**Общая задача**: от пьезоэлементов отходят "волны", которые при благоприятных условиях столкнутся и образуют сильный всплеск как раз в районе дефекта; это столкновение произойдёт в некоторый неизвестный заранее момент времени, который требуется выявить визуально (чтобы локализовать дефект). Для этого рекомендуется сначала проверить 200-500 временных отметок на достаточно большом диапазоне, потом сузить диапазон в 3 раза (взять тот кусок, где явно была активность) и проверить на нём 200-400 отметок; после этого можно ещё раз сузить диапазон и взять больше/меньше отметок уже для демонстрационных целей. В таком случае всего потребуется использовать не более 1500 временных отметок.

## Example

**Start:**

![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/gifs/start.gif)

**Result 1.0.0:**

![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/gifs/result.gif)

**Result 1.1.0:**

![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/gifs/result2.gif)


## Heatmaps

![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20viridis.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20plasma.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20inferno.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20magma.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20cividis.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Greys.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Purples.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Blues.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Greens.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Oranges.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Reds.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20YlOrBr.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20YlOrRd.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20OrRd.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20PuRd.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20RdPu.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20BuPu.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20GnBu.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20PuBu.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20YlGnBu.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20PuBuGn.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20BuGn.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20YlGn.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20binary.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gist_yarg.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gist_gray.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gray.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20bone.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20pink.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20spring.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20summer.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20autumn.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20winter.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20cool.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Wistia.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20hot.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20afmhot.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gist_heat.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20copper.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20PiYG.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20PRGn.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20BrBG.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20PuOr.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20RdGy.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20RdBu.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20RdYlBu.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20RdYlGn.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Spectral.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20coolwarm.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20bwr.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20seismic.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20twilight.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20twilight_shifted.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20hsv.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Pastel1.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Pastel2.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Paired.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Accent.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Dark2.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Set1.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Set2.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20Set3.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20tab10.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20tab20.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20tab20b.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20tab20c.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20flag.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20prism.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20ocean.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gist_earth.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20terrain.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gist_stern.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gnuplot.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gnuplot2.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20CMRmap.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20cubehelix.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20brg.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gist_rainbow.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20rainbow.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20jet.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20nipy_spectral.png)
![1](https://github.com/PasaOpasen/Wave-animation-from-svd/blob/master/images/cmap%20%3D%20gist_ncar.png)










