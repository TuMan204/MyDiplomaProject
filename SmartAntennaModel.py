import numpy as np
import matplotlib.pyplot as plt

# ИСХОДНЫЕ ДАННЫЕ
Fnes = 2.5e9                        # несущ. частота
c = 3e8                             # скор.света
lamda = c/Fnes                      # длина волны
d = lamda/2                         # расстояние между элементами
k = 2*np.pi/lamda                   # волновое число
Fd = Fnes*6                         # частота дискретизации
N = 2048                            # число отсчетов
SNRdB = 30                          # SNR
NumElem = 14                        # кол-во эл-тов АР
NumDOA = 3                          # кол-во ИРИ
dt = np.zeros(N)                    # сетка времени
for i in range(N):
    dt[i] = i/Fd
ElemArr = (np.arange(NumElem)).T    # массив элементов АР
DoAs = np.array([-10, 0, 10])       # углы прихода сигналов
DoAs = np.radians(DoAs)
sinDoAs = np.sin(DoAs)

# МОДЕЛЬ СИГНАЛА
Signal = np.zeros((NumDOA, N), dtype=complex)
for i in range(NumDOA):
    for j in range(N):
        Signal[i, j] = np.exp(1j*2*np.pi
                              * Fnes
                              * dt[j])                  # генерируемый сигнал

AWGN = np.random.randn(NumElem, N) * 10**(-SNRdB/20)    # FIXME: уточнить

A = np.zeros((NumElem, NumDOA), dtype=complex)
for i in range(NumDOA):
    A[:, i] = np.exp(1j*2*np.pi
                     * (d/lamda)
                     * sinDoAs[i]*ElemArr)              # вектора-гипотезы

RecSignal = np.dot(A, Signal) + AWGN                    # принимаемый сигнал

# КОРРЕЛЯЦИОННАЯ И ОБРАТНАЯ ЕЙ МАТРИЦА
R = np.dot(RecSignal, np.matrix(RecSignal).H)           # корр. матрица
R_1 = np.linalg.pinv(R)                                 # обрат. корр. матрица

# SVD РАЗЛОЖЕНИЕ И ВЫДЕЛЕНИЕ ШУМОВОГО ПОДПРОСТРАНСТВА
U, S, V = np.linalg.svd(R)
Unoise = U[:, 1:]

# ОПРЕДЕЛЕНИЕ СЕКТОРА СКАНИРОВАНИЯ
alpha = np.arange(-90, 90, 0.01)
alpha = np.radians(alpha)
sinAlpha = np.sin(alpha)
X = np.zeros((NumElem, len(alpha)), dtype=complex)
for i in range(len(alpha)):
    X[:, i] = np.exp(1j*2*np.pi
                     * (d/lamda)
                     * sinAlpha[i]*ElemArr)

# CAPON
capon = np.zeros(len(alpha), dtype=complex)
for i in range(len(alpha)):
    capon[i] = 1/(np.dot(np.matrix(np.matrix(X[:, i]).H).T,
                  np.dot(R_1, np.matrix(X[:, i]).T)))

# MUSIC
music = np.zeros(len(alpha), dtype=complex)
for i in range(len(alpha)):
    music[i] = (np.dot(np.matrix(np.matrix(X[:, i]).H).T, np.matrix(X[:, i]).T)
                / np.dot(np.matrix(np.matrix(X[:, i]).H).T,
                np.dot(Unoise, np.dot(np.matrix(Unoise).H,
                                      np.matrix(X[:, i]).T))))

# plots
plt.subplots(figsize=(10, 5), dpi=150)
plt.plot(np.degrees(alpha),
         np.real((capon / max(capon))),
         color='green',
         label='CAPON')
plt.plot(np.degrees(alpha),
         np.real((music / max(music))),
         color='blue',
         label='MUSIC')
plt.grid(color='r',
         linestyle='-',
         linewidth=0.2)
plt.xlabel('Azimuth angles θ (degrees)')
plt.ylabel('Power (pseudo)spectrum (normalized)')
plt.legend()
plt.show()
