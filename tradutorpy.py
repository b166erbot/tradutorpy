import gi
import translate
from os import chdir
from pathlib import Path
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk  # noqa

cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)


def copy(texto: str):
    global cb
    cb.set_text(texto, -1)
    cb.store()


tradutor = translate.Translator('pt-br', 'en')


def obter_texto_buffer(funcao):
    """
    Função que retorna o texto do buffer.
    """
    start = funcao.get_start_iter()
    end = funcao.get_end_iter()
    return funcao.get_text(start, end, True)


class Janela:
    """
    Classe que inicializa a construção da janela.
    """
    def __init__(self):
        # criando objetos
        self.builder = Gtk.Builder()

        # obtendo a interface glade
        self.builder.add_from_file('tradutorpy.glade')

        # obtendo objetos
        self._janela = self.builder.get_object('janela')
        self._buffer = self.builder.get_object('buffer')
        self._buffer2 = self.builder.get_object('buffer2')
        self._status = self.builder.get_object('status')
        self._combobox = self.builder.get_object('combobox1')
        self._combobox2 = self.builder.get_object('combobox2')
        self._apagar = self.builder.get_object('apagar')
        self._traduzir = self.builder.get_object('traduzir')
        self._copiar = self.builder.get_object('copiar')
        self._troca = self.builder.get_object('troca')
        self.selected = False

        # conectando objetos
        self._janela.connect('destroy', Gtk.main_quit)
        self._combobox.connect('changed', self.combobox_alterado)
        self._combobox2.connect('changed', self.combobox2_alterado)
        self._apagar.connect('clicked', self.limpar)
        self._traduzir.connect('clicked', self.traduzir)
        self._copiar.connect('clicked', self.copiar)
        self._troca.connect('clicked', self.trocar)

    def traduzir(self, widget):
        global tradutor
        self._status.set_text('traduzindo..')
        cache = [tradutor.to_lang, tradutor.from_lang]
        if self.cache != cache:
            self.cache = cache
            tradutor = translate.Translator(*self.cache)
        tradução = tradutor.translate(obter_texto_buffer(self._buffer))
        self._buffer2.set_text(tradução)
        self._status.set_text('traduzido')

    def copiar(self, widget):
        copy(obter_texto_buffer(self._buffer2))
        self._status.set_text('copiado')

    def limpar(self, widget):
        self._buffer.set_text('')
        self._buffer2.set_text('')
        self._status.set_text('limpo')

    def status(self, texto):
        self._status.set_text('status: ' + texto)

    def combobox_alterado(self, widget):
        item_ativo = widget.get_active_iter()
        if item_ativo:
            modelo = widget.get_model()
            tradutor.from_lang = modelo[item_ativo][1]

    def combobox2_alterado(self, widget):
        item_ativo = widget.get_active_iter()
        if item_ativo:
            modelo = widget.get_model()
            tradutor.to_lang = modelo[item_ativo][1]

    def trocar(self, widget):
        global tradutor
        cache = self._combobox.get_active()
        self._combobox.set_active(self._combobox2.get_active())
        self._combobox2.set_active(cache)
        cache2 = (
            self._combobox.get_model()[self._combobox.get_active_iter()][1])
        cache3 = (
            self._combobox2.get_model()[self._combobox2.get_active_iter()][1])
        tradutor = translate.Translator(cache3, cache2)
        self.cache = [cache3, cache2]


if __name__ == '__main__':
    local_deste_arquivo = Path(__file__).parent
    chdir(local_deste_arquivo)
    app = Janela()
    app.cache = ['pt-br', 'en']
    Gtk.main()
