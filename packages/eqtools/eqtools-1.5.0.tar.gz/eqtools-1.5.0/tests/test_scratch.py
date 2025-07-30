diff = scipy.sqrt(((out - out_t)**2).max()) / scipy.absolute(out).max()
self.assertLessEqual(diff, tol)


# TODO: The trispline case has an extra 1 non-NaN points here.
# self.assertTrue((scipy.isnan(out) == scipy.isnan(out_t)).all())
res2 = (out - out_t)**2
diff = scipy.sqrt((res2[~scipy.isnan(res2)]).max()) / scipy.absolute(out[~scipy.isnan(out)]).max()
self.assertLessEqual(diff, tol)


# diff = scipy.sqrt(((out - out_t)**2).max()) / scipy.absolute(out).max()
# self.assertTrue((scipy.isnan(out) == scipy.isnan(out_t)).all())
res2 = (out - out_t)**2
diff = scipy.sqrt((res2[~scipy.isnan(res2)]).max()) / scipy.absolute(out[~scipy.isnan(out)]).max()
self.assertLessEqual(diff, tol)


self.assertTrue((scipy.isnan(out) == scipy.isnan(out_t)).all())
diff = scipy.sqrt(((out[~scipy.isnan(out)] - out_t[~scipy.isnan(out)])**2).max()) / scipy.absolute(out[~scipy.isnan(out)]).max()
self.assertLessEqual(diff, tol)


diff = scipy.absolute(out - out_t) / scipy.absolute(out).max()
self.assertLessEqual(diff, tol)