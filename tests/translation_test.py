from googletrans import Translator

dt1 = Translator().translate('como averiguo el tiempo transcurrido desde que se encendio el', src='es')
print(dt1.text)
