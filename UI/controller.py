import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDDAnno(self):
        years = self._model.getAllYear()
        for a in years:
            self._view.ddyear.options.append(ft.dropdown.Option(a))
        self._view.ddshape.disabled = False
        self._view.update_page()

    def fillDDForme(self,e):
        self._view.ddshape.value = None

        forme = self._model.getAllForme(self._view.ddyear.value)
        for f in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(f))
        self._view.update_page()

    def handle_graph(self, e):
        a = self._view.ddyear.value
        s = self._view.ddshape.value

        self._model.buildGraph(a,s)
        nodi, archi = self._model.getNumNE()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Vertici = {nodi} Archi = {archi}"))
        archiadiacenti = self._model.getSumW_node()
        for stato,peso in archiadiacenti:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {stato.id} somma pesi su archi = {peso}"))
        self._view.update_page()

    def handle_path(self, e):
        self._model.computePath()

        self._view.txtOut2.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.solBest)}"))

        for ii in self._model.path_edge:
            self._view.txtOut2.controls.append(ft.Text(
                f"{ii[0].id} --> {ii[1].id}: weight {ii[2]} distance {str(self._model.get_distance_weight(ii))}"))  # ii[2]

        self._view.update_page()