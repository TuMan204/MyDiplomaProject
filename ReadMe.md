# My diploma project
В данной работе рассматривается математическое улучшение разрешающей способности ЦАР с помощью алгоритмов сверхразрешения CAPON, MUSIC, ESPRIT и RootMUSIC.

## Алгоритм CLASSIC (BeamScan)
Метод основан на сканировании лучом АР в пространстве и определении максимума уровня излучения. Низкая разрешающая способность, определяемая шириной основного луча АР и уровней боковых лепестков. Разрешающая способность зависит от ширины основного луча АР и связана с ограничением релеевского разрешения. Недостаток может быть смягчен увеличением количества элементов АР.
Выходная функция Алгоритма CAPON описывается выражением:
![equation](https://latex.codecogs.com/svg.image?P=\frac{A(\theta_k)^H\cdot&space;R\cdot&space;A(\theta_k)}{A(\theta_k)^H\cdot&space;A(\theta_k)}),
где ![equation](https://latex.codecogs.com/svg.image?A(\theta_k)) – вектор-гипотеза в определенном угловом направлении; ![equation](https://latex.codecogs.com/svg.image?R)  – корреляционная матрица принятого сигнала.
Пример пеленгационного рельефа алгоритма CLASSIC приведен на следующем рисунке.
![avatar](https://ia.wampi.ru/2022/04/07/classic_for_md.png)

## Алгоритм CAPON
Алгоритм CAPON относится к группе алгоритмов с последовательной пеленгацией источников излучения.
Выходная функция Алгоритма CAPON описывается выражением:
![equation](https://latex.codecogs.com/svg.image?P=\frac{1}{A(\theta_k)^H\cdot&space;R^{-1}\cdot&space;A(\theta_k)}),
где ![equation](https://latex.codecogs.com/svg.image?A(\theta_k)) – вектор-гипотеза в определенном угловом направлении; ![equation](https://latex.codecogs.com/svg.image?R^{-1})  – обратная корреляционная матрица принятого сигнала.
Пример пеленгационного рельефа алгоритма CAPON приведен на следующем рисунке.
![avatar](https://ia.wampi.ru/2022/04/05/capon_for_md.md.png)

## Алгоритм MUSIC
Алгоритм MUSIC также относится к группе алгоритмов с последовательной пеленгацией источников излучения.
Выходная функция Алгоритма MUSIC описывается выражением:
![equation](https://latex.codecogs.com/svg.image?P=\frac{A(\theta_k)^H\cdot&space;A(\theta_k)}{A(\theta_k)^H\cdot&space;U_0&space;\cdot&space;U^H_0\cdot&space;A(\theta_k)})
где ![equation](https://latex.codecogs.com/svg.image?U_0) – шумовое подпространство корреляционной матрицы; ![equation](https://latex.codecogs.com/svg.image?A(\theta_k)) – вектор-гипотеза в определенном угловом направлении.
Пример пеленгационного рельефа алгоритма CAPON приведен на следующем рисунке.
![avatar](https://ie.wampi.ru/2022/04/05/music_for_md.png)

https://latex.codecogs.com/svg.image?P=\frac{A(\theta_k)^H\cdot&space;R\cdot&space;A(\theta_k)}{A(\theta_k)^H\cdot&space;A(\theta_k)}
