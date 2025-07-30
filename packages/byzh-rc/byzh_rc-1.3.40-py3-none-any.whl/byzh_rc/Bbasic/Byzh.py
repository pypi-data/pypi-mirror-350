class Byzh():
    def __init__(self):
        pass
    def B_get_class_name(self):
        return self.__class__.__name__
    def B_get_byzh_version(self):
        import byzh_rc
        return byzh_rc.__version__

if __name__ == '__main__':
    byzh = Byzh()
    print(byzh.B_get_class_name())
    print(byzh.B_get_byzh_version())