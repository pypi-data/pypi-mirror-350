from elenchos.application.ElenchosApplication import ElenchosApplication


def main() -> int:
    application = ElenchosApplication()
    ret = application.run()

    return ret
