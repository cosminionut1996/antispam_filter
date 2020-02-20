from os.path import abspath, dirname, join
import sys

from spam_filter_app import SpamFilter
from data_loader import build_eval_dataframe, build_full_dataframe, dump_res_file


PRODUCT_NAME = "Superantispaminatorul"
STUDENT = "Ionut_Schifirnet"
ALIAS = "SIMBA_123"
VER = "0.4"

KNN, Bayes, SVM = 'KNN', 'Bayes', 'SVM'

ALG = SVM

def main():
    if '-info' == sys.argv[1]:
        with open(sys.argv[2], 'w') as g:
            s = '{}\n{}\n{}\n{}' \
                .format(
                    PRODUCT_NAME,
                    STUDENT,
                    ALIAS,
                    VER
                )
            g.write(s)
        return 0

    model_path = join(abspath(dirname(__file__)), 'model.bin')

    if '-train' == sys.argv[1]:
        app = SpamFilter(ALG, model_path)
        app.train(build_full_dataframe(sys.argv[2]))
        return 0

    if '-scan' == sys.argv[1]:
        app = SpamFilter(ALG, model_path)
        eval_dataframe = build_eval_dataframe(sys.argv[2])
        res = app.evaluate(eval_dataframe)
        dump_res_file(eval_dataframe, res, sys.argv[3])
        return 0

    if '-validate' == sys.argv[1]:
        app = SpamFilter(ALG, model_path)
        validation_dataframe = build_full_dataframe(sys.argv[2])
        res = app.evaluate(validation_dataframe)
        labels = validation_dataframe.label_num.values

        errors = sum(map(lambda x: abs(x[0]-x[1]), zip(res, labels)))

        n = len(labels)
        errors = 0
        fps = 0
        fns = 0
        fp_names = []
        fn_names = []
        for i in range(n):
            if labels[i] != res[i]:
                errors += 1
                if res[i] > labels[i]:
                    fps += 1
                    fp_names.append(validation_dataframe.filename.values[i])
                else:
                    fns += 1
                    fn_names.append(validation_dataframe.filename.values[i])

        Det = (n - errors) * 100 / n
        Fps = fps * 100 / n
        Fns = fns * 100 / n

        print(
            "Det: {}\n"
            "Fps: {}\n"
            "Fns: {}\n"
            "Fp_names: {}\n"
            "Fn_names: {}\n"
            .format(Det, Fps, Fns, fp_names, fn_names)
        )

        return 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        exit(main())
