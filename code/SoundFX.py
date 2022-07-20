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

    def initMenuSoundtrack(self, Bool):
        if Bool:
            menutrack = 'RoboArena_Menu_Soundtrack.wav'
            self.menutrack = QtMultimedia.QSoundEffect()
            self.menutrack.setSource(QtCore.QUrl.fromLocalFile(menutrack))
            self.menutrack.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
            self.menutrack.setVolume(0.2)  # Choose a value between 0 and 1
            self.menutrack.play()

        else:
            self.menutrack.stop()

    def transitionSound(self):
        transitionSFX = 'transitionSound.wav'
        self.transitionSFX = QtMultimedia.QSoundEffect()
        self.transitionSFX.setSource(QtCore.QUrl.fromLocalFile(transitionSFX))
        self.transitionSFX.setVolume(0.1)  # Choose a value between 0 and 1
        self.transitionSFX.play()