import numpy as np
import matplotlib.pyplot as plt

# ИСХОДНЫЕ ДАННЫЕ
np.random.seed(6)
Fnes = 2.5e9                        # несущ. частота
c = 3e8                             # скор.света
lamda = c/Fnes                      # длина волны
d = lamda/2                         # расстояние между элементами
k = 2*np.pi/lamda                   # волновое число
Fd = Fnes*6                         # частота дискретизации
N = 2048                            # число отсчетов
SNRdB = 10                          # SNR
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
QPSKcode = np.zeros((NumDOA, N))                        # формир. QPSK кода
for i in range(NumDOA):
    QPSKcode[i, :] = np.random.randint(0, 4, N)
QPSKphase = np.radians(QPSKcode*360/4+45)
Signal = np.zeros((NumDOA, N), dtype=complex)           # QPSK сигнал
for i in range(NumDOA):
    for j in range(N):
        Signal[i, j] = (np.cos(2*np.pi*Fnes*dt[j]+QPSKphase[i, j])
                        + 1j*np.sin(2*np.pi*Fnes*dt[j]+QPSKphase[i, j]))
# Signal = np.zeros((NumDOA, N), dtype=complex)
# for i in range(NumDOA):
#     for j in range(N):
#         Signal[i, j] = np.sin(2*np.pi
#                               * Fnes
#                               * dt[j])                  # синус. сигнал

AWGN = np.random.randn(NumElem, N) * 10**(-SNRdB/20)    # Аддитивный БГШ

A = np.zeros((NumElem, NumDOA), dtype=complex)
for i in range(NumDOA):
    A[:, i] = np.exp(1j*2*np.pi
                     * (d/lamda)
                     * sinDoAs[i]*ElemArr)              # вектора прихода сигн.

Parr = np.random.randint(5, 10, size=NumDOA)            # мощности сигналов
P = np.diag(Parr)

RecSignal = np.dot(A, np.dot(P, Signal)) + AWGN         # принимаемый сигнал

# КОРРЕЛЯЦИОННАЯ И ОБРАТНАЯ ЕЙ МАТРИЦА
R = np.dot(RecSignal, np.matrix(RecSignal).H)           # корр. матрица
R_1 = np.linalg.pinv(R)                                 # обрат. корр. матрица

# SVD РАЗЛОЖЕНИЕ И ВЫДЕЛЕНИЕ ШУМОВОГО ПОДПРОСТРАНСТВА
U, S, V = np.linalg.svd(R)
Unoise = U[:, NumDOA:]

# ОПРЕДЕЛЕНИЕ СЕКТОРА СКАНИРОВАНИЯ
alpha = np.arange(-90, 90, 0.01)
alpha = np.radians(alpha)
sinAlpha = np.sin(alpha)
X = np.zeros((NumElem, len(alpha)), dtype=complex)
for i in range(len(alpha)):
    X[:, i] = np.exp(1j*2*np.pi
                     * (d/lamda)
                     * sinAlpha[i]*ElemArr)

# CLASSIC
classic = np.zeros(len(alpha), dtype=complex)
for i in range(len(alpha)):
    classic[i] = ((np.dot(np.matrix(np.matrix(X[:, i]).H).T,
                   np.dot(R, np.matrix(X[:, i]).T)))
                  / (np.dot(np.matrix(np.matrix(X[:, i]).H).T,
                     np.matrix(X[:, i]).T)))

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

# ESPRIT
Usig = U[:, :NumDOA]
UsigX = np.linalg.pinv(np.matrix(Usig[:(NumElem-1), :]).T)
UsigY = np.matrix(Usig[1:, :]).T
Psi = np.dot(UsigY, UsigX)
Spsi, Vpsi = np.linalg.eig(Psi)
phi = np.zeros((len(Spsi)))
for i in range(len(Spsi)):
    phi[i] = np.arcsin(np.angle(Spsi[i])/np.pi)
esprit = np.degrees(phi)

# RootMUSIC
C = np.dot(Unoise, np.matrix(Unoise).H)
C_l = np.zeros(2*len(C)-1, dtype=complex)
for i in range(2*len(C)-1):
    Cprom = np.diagonal(C, offset=(i-len(C)+1))
    for j in range(len(Cprom)):
        C_l[i] = C_l[i] + Cprom[j]
z = np.roots(C_l)
j = 0
for i in range(len(z)):
    if np.abs(z[i]) < 1:
        j = j+1
z1 = np.zeros(j, dtype=complex)
j = 0
for i in range(len(z)):
    if np.abs(z[i]) < 1:
        z1[j] = z[i]
        j = j+1
z2 = np.argsort(np.abs(np.abs(z1)-1))
z3 = z2[:NumDOA]
z4 = z1[z3]
z5 = np.zeros(len(z4))
for i in range(len(z4)):
    z5[i] = np.arcsin(np.angle(z4[i])/np.pi)
rootmusic = np.degrees(np.sort(z5))*(-1)

# Plots
plt.subplots(figsize=(10, 5), dpi=150)
# plt.plot(np.real(Signal[0, :]),
#          color='green',
#          label='Signal')
plt.plot(np.degrees(alpha),
         np.real((classic / max(classic))),
         color='crimson',
         label='CLASSIC')
plt.plot(np.degrees(alpha),
         np.real((capon / max(capon))),
         color='green',
         label='CAPON')
plt.plot(np.degrees(alpha),
         np.real((music / max(music))),
         color='blue',
         label='MUSIC')
plt.plot(esprit,
         np.ones(len(esprit)),
         'x',
         color='black',
         label='ESPRIT')
plt.plot(rootmusic,
         np.ones(len(rootmusic))*0.98,
         '.',
         color='purple',
         label='RootMUSIC')
plt.grid(color='r',
         linestyle='-',
         linewidth=0.2)
plt.xlabel('Azimuth angles θ (degrees)')
plt.ylabel('Power (pseudo)spectrum (normalized)')
plt.legend()
plt.show()
