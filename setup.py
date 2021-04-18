from cx_Freeze import setup, Executable


options = {
	"no_compress": False,
	"silent":True
}

setup(
	name = "VPEditor",
	version = "1.2",
	options = {"build_exe":options},
	description = "Editeur web developpe par Nkouanang porel",
	executables = [
		Executable(
			script="D:\\Projets python\\PyQt5_\\VPEditor\\VPEditor.pyw",
			icon = "D:\\Projets python\\PyQt5_\\VPEditor\\images\\logo-bleu.ico"
		)
	]
)