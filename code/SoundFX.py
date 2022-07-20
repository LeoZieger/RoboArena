from PyQt5 import QtCore, QtMultimedia


class SoundFX:
    def initPwrUpSound(self):
        powerupsound = 'PowerUpZap.wav'
        self.powerupsound = QtMultimedia.QSoundEffect()
        self.powerupsound.setSource(QtCore.QUrl.fromLocalFile(powerupsound))
        self.powerupsound.setVolume(0.3)  # Choose a value between 0 and 1
        self.powerupsound.play()

    def initSoundrack(self):
        # This is the part where we can setup the soundtrack
        soundtrack = 'RoboArena_Soundtrack_Demo.wav'
        self.soundtrack = QtMultimedia.QSoundEffect()
        self.soundtrack.setSource(QtCore.QUrl.fromLocalFile(soundtrack))
        self.soundtrack.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
        self.soundtrack.setVolume(0.3)    # Choose a value between 0 and 1
        self.soundtrack.play()
