from PyQt5 import QtCore, QtMultimedia
from PathUtil import getPath


# This is our class, where we define our SoundFX.
# These will later be used in other classes, mainly
# Robo Arena.
class SoundFX:
    # Sound when u get a powerup
    def initPwrUpSound(self):
        powerupsound = getPath("res", "PowerUpZap.wav")
        self.powerupsound = QtMultimedia.QSoundEffect()
        self.powerupsound.setSource(QtCore.QUrl.fromLocalFile(powerupsound))
        self.powerupsound.setVolume(0.3)  # Choose a value between 0 and 1
        self.powerupsound.play()

    # Ingame Soundtrack
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

    # Menu Soundtrack
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

    # This is a small transition-sound after the game is over
    def transitionSound(self):
        transitionSFX = getPath("res", "transitionSound.wav")
        self.transitionSFX = QtMultimedia.QSoundEffect()
        self.transitionSFX.setSource(QtCore.QUrl.fromLocalFile(transitionSFX))
        self.transitionSFX.setVolume(0.1)  # Choose a value between 0 and 1
        self.transitionSFX.play()

    # NOT USED YET
    def initWinningScreen(self):
        winningScreenSFX = getPath("res", "RoboArena_WinningScreen.wav")
        self.winningScreenSFX = QtMultimedia.QSoundEffect()
        self.winningScreenSFX.setSource(QtCore.QUrl.fromLocalFile(winningScreenSFX))
        self.winningScreenSFX.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
        self.winningScreenSFX.setVolume(0.1)  # Choose a value between 0 and 1
        self.winningScreenSFX.play()

    # Shooting Sound for enemy&player
    def shootingEnemySound(self):
        QtMultimedia.QSound.play(enemyShootingFX)

    def shootingSound(self):
        QtMultimedia.QSound.play(shootingFX)


# Implemented the shooting-sound, otherwise the latency would
# be to big
shootingFX = getPath("res", "shooting.wav")
enemyShootingFX = getPath("res", "shootingEnemy.wav")
