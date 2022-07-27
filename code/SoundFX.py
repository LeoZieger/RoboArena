from PyQt5 import QtCore, QtMultimedia
from PathUtil import getPath


class SoundFX:
    def initPwrUpSound(self):
        powerupsound = getPath("res", "PowerUpZap.wav")
        self.powerupsound = QtMultimedia.QSoundEffect()
        self.powerupsound.setSource(QtCore.QUrl.fromLocalFile(powerupsound))
        self.powerupsound.setVolume(0.3)  # Choose a value between 0 and 1
        self.powerupsound.play()

    def initSoundrack(self, bool):
        # This is the part where we can setup the soundtrack
        if bool:
            soundtrack = getPath("res", "RoboArena_Soundtrack_Demo.wav")
            self.soundtrack = QtMultimedia.QSoundEffect()
            self.soundtrack.setSource(QtCore.QUrl.fromLocalFile(soundtrack))
            self.soundtrack.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
            self.soundtrack.setVolume(0.3)    # Choose a value between 0 and 1
            self.soundtrack.play()
        else:
            self.soundtrack.stop()

    def initMenuSoundtrack(self, bool):
        if bool:
            menutrack = getPath("res", "RoboArena_Menu_Soundtrack.wav")
            self.menutrack = QtMultimedia.QSoundEffect()
            self.menutrack.setSource(QtCore.QUrl.fromLocalFile(menutrack))
            self.menutrack.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
            self.menutrack.setVolume(0.2)  # Choose a value between 0 and 1
            self.menutrack.play()

        else:
            self.menutrack.stop()

    def transitionSound(self):
        transitionSFX = getPath("res", "transitionSound.wav")
        self.transitionSFX = QtMultimedia.QSoundEffect()
        self.transitionSFX.setSource(QtCore.QUrl.fromLocalFile(transitionSFX))
        self.transitionSFX.setVolume(0.1)  # Choose a value between 0 and 1
        self.transitionSFX.play()


    def initWinningScreen(self):
        winningScreenSFX = getPath("res", "RoboArena_WinningScreen.wav")
        self.winningScreenSFX = QtMultimedia.QSoundEffect()
        self.winningScreenSFX.setSource(QtCore.QUrl.fromLocalFile(winningScreenSFX))
        self.winningScreenSFX.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
        self.winningScreenSFX.setVolume(0.1)  # Choose a value between 0 and 1
        self.winningScreenSFX.play()

    def shootingEnemySound(self):
        QtMultimedia.QSound.play(enemyShootingFX)

    def shootingSound(self):
        QtMultimedia.QSound.play(shootingFX)


shootingFX = getPath("res", "shooting.wav")
enemyShootingFX = getPath("res", "shootingEnemy.wav")
